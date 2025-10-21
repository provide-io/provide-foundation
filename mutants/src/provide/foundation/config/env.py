# provide/foundation/config/env.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Callable
import os
from typing import Any, Self, TypeVar

from attrs import fields

from provide.foundation.config.base import BaseConfig, field
from provide.foundation.config.types import ConfigSource

"""Environment variable configuration utilities."""


T = TypeVar("T")
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


def x_get_env__mutmut_orig(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_1(
    var_name: str,
    default: str | None = None,
    required: bool = True,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_2(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = False,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_3(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = None

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_4(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(None)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_5(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is not None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_6(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(None)
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_7(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file or value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_8(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith(None):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_9(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("XXfile://XX"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_10(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("FILE://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_11(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = None  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_12(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[8:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_13(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = None
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_14(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(None, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_15(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default=None).strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_16(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_17(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, ).strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_18(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="XXXX").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_19(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_20(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(None)
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

    return value


def x_get_env__mutmut_21(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """Get environment variable value with optional file-based secret support.

    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required and not found

    """
    value = os.environ.get(var_name)

    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default

    # Handle file-based secrets synchronously
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        from provide.foundation.file.safe import safe_read_text

        try:
            value = safe_read_text(file_path, default="").strip()
            if not value:
                raise ValueError(f"Secret file is empty: {file_path}")
        except Exception as e:
            raise ValueError(None) from e

    return value

x_get_env__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_env__mutmut_1': x_get_env__mutmut_1, 
    'x_get_env__mutmut_2': x_get_env__mutmut_2, 
    'x_get_env__mutmut_3': x_get_env__mutmut_3, 
    'x_get_env__mutmut_4': x_get_env__mutmut_4, 
    'x_get_env__mutmut_5': x_get_env__mutmut_5, 
    'x_get_env__mutmut_6': x_get_env__mutmut_6, 
    'x_get_env__mutmut_7': x_get_env__mutmut_7, 
    'x_get_env__mutmut_8': x_get_env__mutmut_8, 
    'x_get_env__mutmut_9': x_get_env__mutmut_9, 
    'x_get_env__mutmut_10': x_get_env__mutmut_10, 
    'x_get_env__mutmut_11': x_get_env__mutmut_11, 
    'x_get_env__mutmut_12': x_get_env__mutmut_12, 
    'x_get_env__mutmut_13': x_get_env__mutmut_13, 
    'x_get_env__mutmut_14': x_get_env__mutmut_14, 
    'x_get_env__mutmut_15': x_get_env__mutmut_15, 
    'x_get_env__mutmut_16': x_get_env__mutmut_16, 
    'x_get_env__mutmut_17': x_get_env__mutmut_17, 
    'x_get_env__mutmut_18': x_get_env__mutmut_18, 
    'x_get_env__mutmut_19': x_get_env__mutmut_19, 
    'x_get_env__mutmut_20': x_get_env__mutmut_20, 
    'x_get_env__mutmut_21': x_get_env__mutmut_21
}

def get_env(*args, **kwargs):
    result = _mutmut_trampoline(x_get_env__mutmut_orig, x_get_env__mutmut_mutants, args, kwargs)
    return result 

get_env.__signature__ = _mutmut_signature(x_get_env__mutmut_orig)
x_get_env__mutmut_orig.__name__ = 'x_get_env'


def x_env_field__mutmut_orig(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_1(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = None

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_2(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop(None, {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_3(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", None)

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_4(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop({})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_5(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", )

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_6(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("XXmetadataXX", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_7(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("METADATA", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_8(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["env_var"] = None
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_9(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["XXenv_varXX"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_10(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["ENV_VAR"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_11(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = None
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_12(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["XXenv_prefixXX"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_13(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["ENV_PREFIX"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_14(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = None

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_15(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["XXenv_parserXX"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_16(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["ENV_PARSER"] = parser

    return field(metadata=metadata, **kwargs)


def x_env_field__mutmut_17(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=None, **kwargs)


def x_env_field__mutmut_18(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(**kwargs)


def x_env_field__mutmut_19(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Create a field that can be loaded from environment variables.

    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments

    Returns:
        Field descriptor

    """
    metadata = kwargs.pop("metadata", {})

    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser

    return field(metadata=metadata, )

x_env_field__mutmut_mutants : ClassVar[MutantDict] = {
'x_env_field__mutmut_1': x_env_field__mutmut_1, 
    'x_env_field__mutmut_2': x_env_field__mutmut_2, 
    'x_env_field__mutmut_3': x_env_field__mutmut_3, 
    'x_env_field__mutmut_4': x_env_field__mutmut_4, 
    'x_env_field__mutmut_5': x_env_field__mutmut_5, 
    'x_env_field__mutmut_6': x_env_field__mutmut_6, 
    'x_env_field__mutmut_7': x_env_field__mutmut_7, 
    'x_env_field__mutmut_8': x_env_field__mutmut_8, 
    'x_env_field__mutmut_9': x_env_field__mutmut_9, 
    'x_env_field__mutmut_10': x_env_field__mutmut_10, 
    'x_env_field__mutmut_11': x_env_field__mutmut_11, 
    'x_env_field__mutmut_12': x_env_field__mutmut_12, 
    'x_env_field__mutmut_13': x_env_field__mutmut_13, 
    'x_env_field__mutmut_14': x_env_field__mutmut_14, 
    'x_env_field__mutmut_15': x_env_field__mutmut_15, 
    'x_env_field__mutmut_16': x_env_field__mutmut_16, 
    'x_env_field__mutmut_17': x_env_field__mutmut_17, 
    'x_env_field__mutmut_18': x_env_field__mutmut_18, 
    'x_env_field__mutmut_19': x_env_field__mutmut_19
}

def env_field(*args, **kwargs):
    result = _mutmut_trampoline(x_env_field__mutmut_orig, x_env_field__mutmut_mutants, args, kwargs)
    return result 

env_field.__signature__ = _mutmut_signature(x_env_field__mutmut_orig)
x_env_field__mutmut_orig.__name__ = 'x_env_field'


class RuntimeConfig(BaseConfig):
    """Configuration that can be loaded from environment variables."""

    @classmethod
    def from_env(
        cls,
        prefix: str = "",
        delimiter: str = "_",
        case_sensitive: bool = False,
    ) -> Self:
        """Load configuration from environment variables synchronously.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive

        Returns:
            Configuration instance

        """
        data = {}

        for attr in fields(cls):
            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                # Build from prefix and field name
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper() if not case_sensitive else attr.name

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Get value from environment
            raw_value = os.environ.get(env_var)

            if raw_value is not None:
                value = raw_value
                # Check if it's a file-based secret
                if value.startswith("file://"):
                    # Read synchronously
                    file_path = value[7:]
                    from provide.foundation.file.safe import safe_read_text

                    try:
                        value = safe_read_text(file_path, default="").strip()
                        if not value:
                            raise ValueError(f"Secret file is empty: {file_path}")
                    except Exception as e:
                        raise ValueError(f"Failed to read secret from file '{file_path}': {e}") from e

                # Apply parser if specified
                parser = attr.metadata.get("env_parser")

                if parser:
                    try:
                        value = parser(value)
                    except Exception as e:
                        raise ValueError(f"Failed to parse {env_var}: {e}") from e
                else:
                    # Try to infer parser from type
                    from provide.foundation.parsers import auto_parse

                    value = auto_parse(attr, value)

                data[attr.name] = value

        return cls.from_dict(data, source=ConfigSource.ENV)

    def xǁRuntimeConfigǁto_env_dict__mutmut_orig(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_1(self, prefix: str = "XXXX", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_2(self, prefix: str = "", delimiter: str = "XX_XX") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_3(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = None

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_4(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(None):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_5(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = None

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_6(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(None, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_7(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, None)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_8(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_9(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, )

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_10(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is not None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_11(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                break

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_12(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = None

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_13(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get(None)

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_14(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("XXenv_varXX")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_15(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("ENV_VAR")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_16(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_17(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = None
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_18(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get(None, prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_19(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", None)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_20(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get(prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_21(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", )
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_22(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("XXenv_prefixXX", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_23(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("ENV_PREFIX", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_24(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = None

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_25(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.lower()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_26(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = None

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_27(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = None
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_28(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "XXtrueXX" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_29(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "TRUE" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_30(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "XXfalseXX"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_31(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "FALSE"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_32(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = None
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_33(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(None)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_34(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = "XX,XX".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_35(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(None) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_36(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = None
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_37(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(None)
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_38(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = "XX,XX".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_39(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = None

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_40(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(None)

            env_dict[env_var] = str_value

        return env_dict

    def xǁRuntimeConfigǁto_env_dict__mutmut_41(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """Convert configuration to environment variable dictionary.

        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name

        Returns:
            Dictionary of environment variables

        """
        env_dict = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip None values
            if value is None:
                continue

            # Determine environment variable name
            env_var = attr.metadata.get("env_var")

            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()

                env_var = f"{field_prefix}{delimiter}{field_name}" if field_prefix else field_name

            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)

            env_dict[env_var] = None

        return env_dict
    
    xǁRuntimeConfigǁto_env_dict__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRuntimeConfigǁto_env_dict__mutmut_1': xǁRuntimeConfigǁto_env_dict__mutmut_1, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_2': xǁRuntimeConfigǁto_env_dict__mutmut_2, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_3': xǁRuntimeConfigǁto_env_dict__mutmut_3, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_4': xǁRuntimeConfigǁto_env_dict__mutmut_4, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_5': xǁRuntimeConfigǁto_env_dict__mutmut_5, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_6': xǁRuntimeConfigǁto_env_dict__mutmut_6, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_7': xǁRuntimeConfigǁto_env_dict__mutmut_7, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_8': xǁRuntimeConfigǁto_env_dict__mutmut_8, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_9': xǁRuntimeConfigǁto_env_dict__mutmut_9, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_10': xǁRuntimeConfigǁto_env_dict__mutmut_10, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_11': xǁRuntimeConfigǁto_env_dict__mutmut_11, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_12': xǁRuntimeConfigǁto_env_dict__mutmut_12, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_13': xǁRuntimeConfigǁto_env_dict__mutmut_13, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_14': xǁRuntimeConfigǁto_env_dict__mutmut_14, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_15': xǁRuntimeConfigǁto_env_dict__mutmut_15, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_16': xǁRuntimeConfigǁto_env_dict__mutmut_16, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_17': xǁRuntimeConfigǁto_env_dict__mutmut_17, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_18': xǁRuntimeConfigǁto_env_dict__mutmut_18, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_19': xǁRuntimeConfigǁto_env_dict__mutmut_19, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_20': xǁRuntimeConfigǁto_env_dict__mutmut_20, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_21': xǁRuntimeConfigǁto_env_dict__mutmut_21, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_22': xǁRuntimeConfigǁto_env_dict__mutmut_22, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_23': xǁRuntimeConfigǁto_env_dict__mutmut_23, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_24': xǁRuntimeConfigǁto_env_dict__mutmut_24, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_25': xǁRuntimeConfigǁto_env_dict__mutmut_25, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_26': xǁRuntimeConfigǁto_env_dict__mutmut_26, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_27': xǁRuntimeConfigǁto_env_dict__mutmut_27, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_28': xǁRuntimeConfigǁto_env_dict__mutmut_28, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_29': xǁRuntimeConfigǁto_env_dict__mutmut_29, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_30': xǁRuntimeConfigǁto_env_dict__mutmut_30, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_31': xǁRuntimeConfigǁto_env_dict__mutmut_31, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_32': xǁRuntimeConfigǁto_env_dict__mutmut_32, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_33': xǁRuntimeConfigǁto_env_dict__mutmut_33, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_34': xǁRuntimeConfigǁto_env_dict__mutmut_34, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_35': xǁRuntimeConfigǁto_env_dict__mutmut_35, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_36': xǁRuntimeConfigǁto_env_dict__mutmut_36, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_37': xǁRuntimeConfigǁto_env_dict__mutmut_37, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_38': xǁRuntimeConfigǁto_env_dict__mutmut_38, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_39': xǁRuntimeConfigǁto_env_dict__mutmut_39, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_40': xǁRuntimeConfigǁto_env_dict__mutmut_40, 
        'xǁRuntimeConfigǁto_env_dict__mutmut_41': xǁRuntimeConfigǁto_env_dict__mutmut_41
    }
    
    def to_env_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRuntimeConfigǁto_env_dict__mutmut_orig"), object.__getattribute__(self, "xǁRuntimeConfigǁto_env_dict__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_env_dict.__signature__ = _mutmut_signature(xǁRuntimeConfigǁto_env_dict__mutmut_orig)
    xǁRuntimeConfigǁto_env_dict__mutmut_orig.__name__ = 'xǁRuntimeConfigǁto_env_dict'


# <3 🧱🤝⚙️🪄
