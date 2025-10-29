# provide/foundation/utils/environment/prefix.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, TypeVar

from provide.foundation.utils.caching import LRUCache
from provide.foundation.utils.environment.getters import (
    get_bool,
    get_dict,
    get_float,
    get_int,
    get_list,
    get_path,
    get_str,
    require,
)

"""Environment variable reader with prefix support.

Provides the EnvPrefix class for convenient access to environment variables
with a common prefix, useful for application-specific configuration namespacing.
"""


T = TypeVar("T")
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


class EnvPrefix:
    """Environment variable reader with prefix support.

    Provides convenient access to environment variables with a common prefix,
    useful for application-specific configuration namespacing.

    Uses caching to improve performance for repeated name lookups.

    Examples:
        >>> app_env = EnvPrefix('MYAPP')
        >>> app_env.get_bool('DEBUG')  # Reads MYAPP_DEBUG
        >>> app_env['database_url']  # Reads MYAPP_DATABASE_URL

    """

    def xǁEnvPrefixǁ__init____mutmut_orig(self, prefix: str, separator: str = "_") -> None:
        """Initialize with prefix.

        Args:
            prefix: Prefix for all environment variables
            separator: Separator between prefix and variable name

        """
        self.prefix = prefix.upper()
        self.separator = separator
        self._name_cache = LRUCache(maxsize=128)

    def xǁEnvPrefixǁ__init____mutmut_1(self, prefix: str, separator: str = "XX_XX") -> None:
        """Initialize with prefix.

        Args:
            prefix: Prefix for all environment variables
            separator: Separator between prefix and variable name

        """
        self.prefix = prefix.upper()
        self.separator = separator
        self._name_cache = LRUCache(maxsize=128)

    def xǁEnvPrefixǁ__init____mutmut_2(self, prefix: str, separator: str = "_") -> None:
        """Initialize with prefix.

        Args:
            prefix: Prefix for all environment variables
            separator: Separator between prefix and variable name

        """
        self.prefix = None
        self.separator = separator
        self._name_cache = LRUCache(maxsize=128)

    def xǁEnvPrefixǁ__init____mutmut_3(self, prefix: str, separator: str = "_") -> None:
        """Initialize with prefix.

        Args:
            prefix: Prefix for all environment variables
            separator: Separator between prefix and variable name

        """
        self.prefix = prefix.lower()
        self.separator = separator
        self._name_cache = LRUCache(maxsize=128)

    def xǁEnvPrefixǁ__init____mutmut_4(self, prefix: str, separator: str = "_") -> None:
        """Initialize with prefix.

        Args:
            prefix: Prefix for all environment variables
            separator: Separator between prefix and variable name

        """
        self.prefix = prefix.upper()
        self.separator = None
        self._name_cache = LRUCache(maxsize=128)

    def xǁEnvPrefixǁ__init____mutmut_5(self, prefix: str, separator: str = "_") -> None:
        """Initialize with prefix.

        Args:
            prefix: Prefix for all environment variables
            separator: Separator between prefix and variable name

        """
        self.prefix = prefix.upper()
        self.separator = separator
        self._name_cache = None

    def xǁEnvPrefixǁ__init____mutmut_6(self, prefix: str, separator: str = "_") -> None:
        """Initialize with prefix.

        Args:
            prefix: Prefix for all environment variables
            separator: Separator between prefix and variable name

        """
        self.prefix = prefix.upper()
        self.separator = separator
        self._name_cache = LRUCache(maxsize=None)

    def xǁEnvPrefixǁ__init____mutmut_7(self, prefix: str, separator: str = "_") -> None:
        """Initialize with prefix.

        Args:
            prefix: Prefix for all environment variables
            separator: Separator between prefix and variable name

        """
        self.prefix = prefix.upper()
        self.separator = separator
        self._name_cache = LRUCache(maxsize=129)

    xǁEnvPrefixǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁ__init____mutmut_1": xǁEnvPrefixǁ__init____mutmut_1,
        "xǁEnvPrefixǁ__init____mutmut_2": xǁEnvPrefixǁ__init____mutmut_2,
        "xǁEnvPrefixǁ__init____mutmut_3": xǁEnvPrefixǁ__init____mutmut_3,
        "xǁEnvPrefixǁ__init____mutmut_4": xǁEnvPrefixǁ__init____mutmut_4,
        "xǁEnvPrefixǁ__init____mutmut_5": xǁEnvPrefixǁ__init____mutmut_5,
        "xǁEnvPrefixǁ__init____mutmut_6": xǁEnvPrefixǁ__init____mutmut_6,
        "xǁEnvPrefixǁ__init____mutmut_7": xǁEnvPrefixǁ__init____mutmut_7,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁEnvPrefixǁ__init____mutmut_orig)
    xǁEnvPrefixǁ__init____mutmut_orig.__name__ = "xǁEnvPrefixǁ__init__"

    def xǁEnvPrefixǁ_make_name__mutmut_orig(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_1(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = None
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_2(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(None)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_3(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_4(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = None
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_5(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace(None, "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_6(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace(".", None)
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_7(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace("_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_8(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = (
            name.upper()
            .replace("-", "_")
            .replace(
                ".",
            )
        )
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_9(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace(None, "_").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_10(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", None).replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_11(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("_").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_12(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = (
            name.upper()
            .replace(
                "-",
            )
            .replace(".", "_")
        )
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_13(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.lower().replace("-", "_").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_14(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("XX-XX", "_").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_15(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "XX_XX").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_16(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace("XX.XX", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_17(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace(".", "XX_XX")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_18(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace(".", "_")
        full_name = None

        # Store in cache
        self._name_cache.set(name, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_19(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(None, full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_20(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(name, None)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_21(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(full_name)

        return full_name

    def xǁEnvPrefixǁ_make_name__mutmut_22(self, name: str) -> str:
        """Create full environment variable name.

        Results are cached for improved performance on repeated calls.

        Args:
            name: Variable name to normalize

        Returns:
            Full environment variable name with prefix
        """
        # Check cache first
        cached_name = self._name_cache.get(name)
        if cached_name is not None:
            return cached_name

        # Convert to uppercase and replace common separators
        normalized = name.upper().replace("-", "_").replace(".", "_")
        full_name = f"{self.prefix}{self.separator}{normalized}"

        # Store in cache
        self._name_cache.set(
            name,
        )

        return full_name

    xǁEnvPrefixǁ_make_name__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁ_make_name__mutmut_1": xǁEnvPrefixǁ_make_name__mutmut_1,
        "xǁEnvPrefixǁ_make_name__mutmut_2": xǁEnvPrefixǁ_make_name__mutmut_2,
        "xǁEnvPrefixǁ_make_name__mutmut_3": xǁEnvPrefixǁ_make_name__mutmut_3,
        "xǁEnvPrefixǁ_make_name__mutmut_4": xǁEnvPrefixǁ_make_name__mutmut_4,
        "xǁEnvPrefixǁ_make_name__mutmut_5": xǁEnvPrefixǁ_make_name__mutmut_5,
        "xǁEnvPrefixǁ_make_name__mutmut_6": xǁEnvPrefixǁ_make_name__mutmut_6,
        "xǁEnvPrefixǁ_make_name__mutmut_7": xǁEnvPrefixǁ_make_name__mutmut_7,
        "xǁEnvPrefixǁ_make_name__mutmut_8": xǁEnvPrefixǁ_make_name__mutmut_8,
        "xǁEnvPrefixǁ_make_name__mutmut_9": xǁEnvPrefixǁ_make_name__mutmut_9,
        "xǁEnvPrefixǁ_make_name__mutmut_10": xǁEnvPrefixǁ_make_name__mutmut_10,
        "xǁEnvPrefixǁ_make_name__mutmut_11": xǁEnvPrefixǁ_make_name__mutmut_11,
        "xǁEnvPrefixǁ_make_name__mutmut_12": xǁEnvPrefixǁ_make_name__mutmut_12,
        "xǁEnvPrefixǁ_make_name__mutmut_13": xǁEnvPrefixǁ_make_name__mutmut_13,
        "xǁEnvPrefixǁ_make_name__mutmut_14": xǁEnvPrefixǁ_make_name__mutmut_14,
        "xǁEnvPrefixǁ_make_name__mutmut_15": xǁEnvPrefixǁ_make_name__mutmut_15,
        "xǁEnvPrefixǁ_make_name__mutmut_16": xǁEnvPrefixǁ_make_name__mutmut_16,
        "xǁEnvPrefixǁ_make_name__mutmut_17": xǁEnvPrefixǁ_make_name__mutmut_17,
        "xǁEnvPrefixǁ_make_name__mutmut_18": xǁEnvPrefixǁ_make_name__mutmut_18,
        "xǁEnvPrefixǁ_make_name__mutmut_19": xǁEnvPrefixǁ_make_name__mutmut_19,
        "xǁEnvPrefixǁ_make_name__mutmut_20": xǁEnvPrefixǁ_make_name__mutmut_20,
        "xǁEnvPrefixǁ_make_name__mutmut_21": xǁEnvPrefixǁ_make_name__mutmut_21,
        "xǁEnvPrefixǁ_make_name__mutmut_22": xǁEnvPrefixǁ_make_name__mutmut_22,
    }

    def _make_name(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁ_make_name__mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁ_make_name__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _make_name.__signature__ = _mutmut_signature(xǁEnvPrefixǁ_make_name__mutmut_orig)
    xǁEnvPrefixǁ_make_name__mutmut_orig.__name__ = "xǁEnvPrefixǁ_make_name"

    def xǁEnvPrefixǁget_bool__mutmut_orig(self, name: str, default: bool | None = None) -> bool | None:
        """Get boolean with prefix."""
        return get_bool(self._make_name(name), default)

    def xǁEnvPrefixǁget_bool__mutmut_1(self, name: str, default: bool | None = None) -> bool | None:
        """Get boolean with prefix."""
        return get_bool(None, default)

    def xǁEnvPrefixǁget_bool__mutmut_2(self, name: str, default: bool | None = None) -> bool | None:
        """Get boolean with prefix."""
        return get_bool(self._make_name(name), None)

    def xǁEnvPrefixǁget_bool__mutmut_3(self, name: str, default: bool | None = None) -> bool | None:
        """Get boolean with prefix."""
        return get_bool(default)

    def xǁEnvPrefixǁget_bool__mutmut_4(self, name: str, default: bool | None = None) -> bool | None:
        """Get boolean with prefix."""
        return get_bool(
            self._make_name(name),
        )

    def xǁEnvPrefixǁget_bool__mutmut_5(self, name: str, default: bool | None = None) -> bool | None:
        """Get boolean with prefix."""
        return get_bool(self._make_name(None), default)

    xǁEnvPrefixǁget_bool__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁget_bool__mutmut_1": xǁEnvPrefixǁget_bool__mutmut_1,
        "xǁEnvPrefixǁget_bool__mutmut_2": xǁEnvPrefixǁget_bool__mutmut_2,
        "xǁEnvPrefixǁget_bool__mutmut_3": xǁEnvPrefixǁget_bool__mutmut_3,
        "xǁEnvPrefixǁget_bool__mutmut_4": xǁEnvPrefixǁget_bool__mutmut_4,
        "xǁEnvPrefixǁget_bool__mutmut_5": xǁEnvPrefixǁget_bool__mutmut_5,
    }

    def get_bool(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁget_bool__mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁget_bool__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_bool.__signature__ = _mutmut_signature(xǁEnvPrefixǁget_bool__mutmut_orig)
    xǁEnvPrefixǁget_bool__mutmut_orig.__name__ = "xǁEnvPrefixǁget_bool"

    def xǁEnvPrefixǁget_int__mutmut_orig(self, name: str, default: int | None = None) -> int | None:
        """Get integer with prefix."""
        return get_int(self._make_name(name), default)

    def xǁEnvPrefixǁget_int__mutmut_1(self, name: str, default: int | None = None) -> int | None:
        """Get integer with prefix."""
        return get_int(None, default)

    def xǁEnvPrefixǁget_int__mutmut_2(self, name: str, default: int | None = None) -> int | None:
        """Get integer with prefix."""
        return get_int(self._make_name(name), None)

    def xǁEnvPrefixǁget_int__mutmut_3(self, name: str, default: int | None = None) -> int | None:
        """Get integer with prefix."""
        return get_int(default)

    def xǁEnvPrefixǁget_int__mutmut_4(self, name: str, default: int | None = None) -> int | None:
        """Get integer with prefix."""
        return get_int(
            self._make_name(name),
        )

    def xǁEnvPrefixǁget_int__mutmut_5(self, name: str, default: int | None = None) -> int | None:
        """Get integer with prefix."""
        return get_int(self._make_name(None), default)

    xǁEnvPrefixǁget_int__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁget_int__mutmut_1": xǁEnvPrefixǁget_int__mutmut_1,
        "xǁEnvPrefixǁget_int__mutmut_2": xǁEnvPrefixǁget_int__mutmut_2,
        "xǁEnvPrefixǁget_int__mutmut_3": xǁEnvPrefixǁget_int__mutmut_3,
        "xǁEnvPrefixǁget_int__mutmut_4": xǁEnvPrefixǁget_int__mutmut_4,
        "xǁEnvPrefixǁget_int__mutmut_5": xǁEnvPrefixǁget_int__mutmut_5,
    }

    def get_int(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁget_int__mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁget_int__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_int.__signature__ = _mutmut_signature(xǁEnvPrefixǁget_int__mutmut_orig)
    xǁEnvPrefixǁget_int__mutmut_orig.__name__ = "xǁEnvPrefixǁget_int"

    def xǁEnvPrefixǁget_float__mutmut_orig(self, name: str, default: float | None = None) -> float | None:
        """Get float with prefix."""
        return get_float(self._make_name(name), default)

    def xǁEnvPrefixǁget_float__mutmut_1(self, name: str, default: float | None = None) -> float | None:
        """Get float with prefix."""
        return get_float(None, default)

    def xǁEnvPrefixǁget_float__mutmut_2(self, name: str, default: float | None = None) -> float | None:
        """Get float with prefix."""
        return get_float(self._make_name(name), None)

    def xǁEnvPrefixǁget_float__mutmut_3(self, name: str, default: float | None = None) -> float | None:
        """Get float with prefix."""
        return get_float(default)

    def xǁEnvPrefixǁget_float__mutmut_4(self, name: str, default: float | None = None) -> float | None:
        """Get float with prefix."""
        return get_float(
            self._make_name(name),
        )

    def xǁEnvPrefixǁget_float__mutmut_5(self, name: str, default: float | None = None) -> float | None:
        """Get float with prefix."""
        return get_float(self._make_name(None), default)

    xǁEnvPrefixǁget_float__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁget_float__mutmut_1": xǁEnvPrefixǁget_float__mutmut_1,
        "xǁEnvPrefixǁget_float__mutmut_2": xǁEnvPrefixǁget_float__mutmut_2,
        "xǁEnvPrefixǁget_float__mutmut_3": xǁEnvPrefixǁget_float__mutmut_3,
        "xǁEnvPrefixǁget_float__mutmut_4": xǁEnvPrefixǁget_float__mutmut_4,
        "xǁEnvPrefixǁget_float__mutmut_5": xǁEnvPrefixǁget_float__mutmut_5,
    }

    def get_float(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁget_float__mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁget_float__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_float.__signature__ = _mutmut_signature(xǁEnvPrefixǁget_float__mutmut_orig)
    xǁEnvPrefixǁget_float__mutmut_orig.__name__ = "xǁEnvPrefixǁget_float"

    def xǁEnvPrefixǁget_str__mutmut_orig(self, name: str, default: str | None = None) -> str | None:
        """Get string with prefix."""
        return get_str(self._make_name(name), default)

    def xǁEnvPrefixǁget_str__mutmut_1(self, name: str, default: str | None = None) -> str | None:
        """Get string with prefix."""
        return get_str(None, default)

    def xǁEnvPrefixǁget_str__mutmut_2(self, name: str, default: str | None = None) -> str | None:
        """Get string with prefix."""
        return get_str(self._make_name(name), None)

    def xǁEnvPrefixǁget_str__mutmut_3(self, name: str, default: str | None = None) -> str | None:
        """Get string with prefix."""
        return get_str(default)

    def xǁEnvPrefixǁget_str__mutmut_4(self, name: str, default: str | None = None) -> str | None:
        """Get string with prefix."""
        return get_str(
            self._make_name(name),
        )

    def xǁEnvPrefixǁget_str__mutmut_5(self, name: str, default: str | None = None) -> str | None:
        """Get string with prefix."""
        return get_str(self._make_name(None), default)

    xǁEnvPrefixǁget_str__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁget_str__mutmut_1": xǁEnvPrefixǁget_str__mutmut_1,
        "xǁEnvPrefixǁget_str__mutmut_2": xǁEnvPrefixǁget_str__mutmut_2,
        "xǁEnvPrefixǁget_str__mutmut_3": xǁEnvPrefixǁget_str__mutmut_3,
        "xǁEnvPrefixǁget_str__mutmut_4": xǁEnvPrefixǁget_str__mutmut_4,
        "xǁEnvPrefixǁget_str__mutmut_5": xǁEnvPrefixǁget_str__mutmut_5,
    }

    def get_str(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁget_str__mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁget_str__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_str.__signature__ = _mutmut_signature(xǁEnvPrefixǁget_str__mutmut_orig)
    xǁEnvPrefixǁget_str__mutmut_orig.__name__ = "xǁEnvPrefixǁget_str"

    def xǁEnvPrefixǁget_path__mutmut_orig(self, name: str, default: Path | str | None = None) -> Path | None:
        """Get path with prefix."""
        return get_path(self._make_name(name), default)

    def xǁEnvPrefixǁget_path__mutmut_1(self, name: str, default: Path | str | None = None) -> Path | None:
        """Get path with prefix."""
        return get_path(None, default)

    def xǁEnvPrefixǁget_path__mutmut_2(self, name: str, default: Path | str | None = None) -> Path | None:
        """Get path with prefix."""
        return get_path(self._make_name(name), None)

    def xǁEnvPrefixǁget_path__mutmut_3(self, name: str, default: Path | str | None = None) -> Path | None:
        """Get path with prefix."""
        return get_path(default)

    def xǁEnvPrefixǁget_path__mutmut_4(self, name: str, default: Path | str | None = None) -> Path | None:
        """Get path with prefix."""
        return get_path(
            self._make_name(name),
        )

    def xǁEnvPrefixǁget_path__mutmut_5(self, name: str, default: Path | str | None = None) -> Path | None:
        """Get path with prefix."""
        return get_path(self._make_name(None), default)

    xǁEnvPrefixǁget_path__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁget_path__mutmut_1": xǁEnvPrefixǁget_path__mutmut_1,
        "xǁEnvPrefixǁget_path__mutmut_2": xǁEnvPrefixǁget_path__mutmut_2,
        "xǁEnvPrefixǁget_path__mutmut_3": xǁEnvPrefixǁget_path__mutmut_3,
        "xǁEnvPrefixǁget_path__mutmut_4": xǁEnvPrefixǁget_path__mutmut_4,
        "xǁEnvPrefixǁget_path__mutmut_5": xǁEnvPrefixǁget_path__mutmut_5,
    }

    def get_path(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁget_path__mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁget_path__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_path.__signature__ = _mutmut_signature(xǁEnvPrefixǁget_path__mutmut_orig)
    xǁEnvPrefixǁget_path__mutmut_orig.__name__ = "xǁEnvPrefixǁget_path"

    def xǁEnvPrefixǁget_list__mutmut_orig(
        self, name: str, default: list[str] | None = None, separator: str = ","
    ) -> list[str]:
        """Get list with prefix."""
        return get_list(self._make_name(name), default, separator)

    def xǁEnvPrefixǁget_list__mutmut_1(
        self, name: str, default: list[str] | None = None, separator: str = "XX,XX"
    ) -> list[str]:
        """Get list with prefix."""
        return get_list(self._make_name(name), default, separator)

    def xǁEnvPrefixǁget_list__mutmut_2(
        self, name: str, default: list[str] | None = None, separator: str = ","
    ) -> list[str]:
        """Get list with prefix."""
        return get_list(None, default, separator)

    def xǁEnvPrefixǁget_list__mutmut_3(
        self, name: str, default: list[str] | None = None, separator: str = ","
    ) -> list[str]:
        """Get list with prefix."""
        return get_list(self._make_name(name), None, separator)

    def xǁEnvPrefixǁget_list__mutmut_4(
        self, name: str, default: list[str] | None = None, separator: str = ","
    ) -> list[str]:
        """Get list with prefix."""
        return get_list(self._make_name(name), default, None)

    def xǁEnvPrefixǁget_list__mutmut_5(
        self, name: str, default: list[str] | None = None, separator: str = ","
    ) -> list[str]:
        """Get list with prefix."""
        return get_list(default, separator)

    def xǁEnvPrefixǁget_list__mutmut_6(
        self, name: str, default: list[str] | None = None, separator: str = ","
    ) -> list[str]:
        """Get list with prefix."""
        return get_list(self._make_name(name), separator)

    def xǁEnvPrefixǁget_list__mutmut_7(
        self, name: str, default: list[str] | None = None, separator: str = ","
    ) -> list[str]:
        """Get list with prefix."""
        return get_list(
            self._make_name(name),
            default,
        )

    def xǁEnvPrefixǁget_list__mutmut_8(
        self, name: str, default: list[str] | None = None, separator: str = ","
    ) -> list[str]:
        """Get list with prefix."""
        return get_list(self._make_name(None), default, separator)

    xǁEnvPrefixǁget_list__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁget_list__mutmut_1": xǁEnvPrefixǁget_list__mutmut_1,
        "xǁEnvPrefixǁget_list__mutmut_2": xǁEnvPrefixǁget_list__mutmut_2,
        "xǁEnvPrefixǁget_list__mutmut_3": xǁEnvPrefixǁget_list__mutmut_3,
        "xǁEnvPrefixǁget_list__mutmut_4": xǁEnvPrefixǁget_list__mutmut_4,
        "xǁEnvPrefixǁget_list__mutmut_5": xǁEnvPrefixǁget_list__mutmut_5,
        "xǁEnvPrefixǁget_list__mutmut_6": xǁEnvPrefixǁget_list__mutmut_6,
        "xǁEnvPrefixǁget_list__mutmut_7": xǁEnvPrefixǁget_list__mutmut_7,
        "xǁEnvPrefixǁget_list__mutmut_8": xǁEnvPrefixǁget_list__mutmut_8,
    }

    def get_list(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁget_list__mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁget_list__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_list.__signature__ = _mutmut_signature(xǁEnvPrefixǁget_list__mutmut_orig)
    xǁEnvPrefixǁget_list__mutmut_orig.__name__ = "xǁEnvPrefixǁget_list"

    def xǁEnvPrefixǁget_dict__mutmut_orig(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = ",",
        key_value_separator: str = "=",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(self._make_name(name), default, item_separator, key_value_separator)

    def xǁEnvPrefixǁget_dict__mutmut_1(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = "XX,XX",
        key_value_separator: str = "=",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(self._make_name(name), default, item_separator, key_value_separator)

    def xǁEnvPrefixǁget_dict__mutmut_2(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = ",",
        key_value_separator: str = "XX=XX",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(self._make_name(name), default, item_separator, key_value_separator)

    def xǁEnvPrefixǁget_dict__mutmut_3(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = ",",
        key_value_separator: str = "=",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(None, default, item_separator, key_value_separator)

    def xǁEnvPrefixǁget_dict__mutmut_4(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = ",",
        key_value_separator: str = "=",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(self._make_name(name), None, item_separator, key_value_separator)

    def xǁEnvPrefixǁget_dict__mutmut_5(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = ",",
        key_value_separator: str = "=",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(self._make_name(name), default, None, key_value_separator)

    def xǁEnvPrefixǁget_dict__mutmut_6(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = ",",
        key_value_separator: str = "=",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(self._make_name(name), default, item_separator, None)

    def xǁEnvPrefixǁget_dict__mutmut_7(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = ",",
        key_value_separator: str = "=",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(default, item_separator, key_value_separator)

    def xǁEnvPrefixǁget_dict__mutmut_8(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = ",",
        key_value_separator: str = "=",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(self._make_name(name), item_separator, key_value_separator)

    def xǁEnvPrefixǁget_dict__mutmut_9(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = ",",
        key_value_separator: str = "=",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(self._make_name(name), default, key_value_separator)

    def xǁEnvPrefixǁget_dict__mutmut_10(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = ",",
        key_value_separator: str = "=",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(
            self._make_name(name),
            default,
            item_separator,
        )

    def xǁEnvPrefixǁget_dict__mutmut_11(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = ",",
        key_value_separator: str = "=",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(self._make_name(None), default, item_separator, key_value_separator)

    xǁEnvPrefixǁget_dict__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁget_dict__mutmut_1": xǁEnvPrefixǁget_dict__mutmut_1,
        "xǁEnvPrefixǁget_dict__mutmut_2": xǁEnvPrefixǁget_dict__mutmut_2,
        "xǁEnvPrefixǁget_dict__mutmut_3": xǁEnvPrefixǁget_dict__mutmut_3,
        "xǁEnvPrefixǁget_dict__mutmut_4": xǁEnvPrefixǁget_dict__mutmut_4,
        "xǁEnvPrefixǁget_dict__mutmut_5": xǁEnvPrefixǁget_dict__mutmut_5,
        "xǁEnvPrefixǁget_dict__mutmut_6": xǁEnvPrefixǁget_dict__mutmut_6,
        "xǁEnvPrefixǁget_dict__mutmut_7": xǁEnvPrefixǁget_dict__mutmut_7,
        "xǁEnvPrefixǁget_dict__mutmut_8": xǁEnvPrefixǁget_dict__mutmut_8,
        "xǁEnvPrefixǁget_dict__mutmut_9": xǁEnvPrefixǁget_dict__mutmut_9,
        "xǁEnvPrefixǁget_dict__mutmut_10": xǁEnvPrefixǁget_dict__mutmut_10,
        "xǁEnvPrefixǁget_dict__mutmut_11": xǁEnvPrefixǁget_dict__mutmut_11,
    }

    def get_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁget_dict__mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁget_dict__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_dict.__signature__ = _mutmut_signature(xǁEnvPrefixǁget_dict__mutmut_orig)
    xǁEnvPrefixǁget_dict__mutmut_orig.__name__ = "xǁEnvPrefixǁget_dict"

    def xǁEnvPrefixǁrequire__mutmut_orig(self, name: str, type_hint: type[T] | None = None) -> Any:
        """Require variable with prefix."""
        return require(self._make_name(name), type_hint)

    def xǁEnvPrefixǁrequire__mutmut_1(self, name: str, type_hint: type[T] | None = None) -> Any:
        """Require variable with prefix."""
        return require(None, type_hint)

    def xǁEnvPrefixǁrequire__mutmut_2(self, name: str, type_hint: type[T] | None = None) -> Any:
        """Require variable with prefix."""
        return require(self._make_name(name), None)

    def xǁEnvPrefixǁrequire__mutmut_3(self, name: str, type_hint: type[T] | None = None) -> Any:
        """Require variable with prefix."""
        return require(type_hint)

    def xǁEnvPrefixǁrequire__mutmut_4(self, name: str, type_hint: type[T] | None = None) -> Any:
        """Require variable with prefix."""
        return require(
            self._make_name(name),
        )

    def xǁEnvPrefixǁrequire__mutmut_5(self, name: str, type_hint: type[T] | None = None) -> Any:
        """Require variable with prefix."""
        return require(self._make_name(None), type_hint)

    xǁEnvPrefixǁrequire__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁrequire__mutmut_1": xǁEnvPrefixǁrequire__mutmut_1,
        "xǁEnvPrefixǁrequire__mutmut_2": xǁEnvPrefixǁrequire__mutmut_2,
        "xǁEnvPrefixǁrequire__mutmut_3": xǁEnvPrefixǁrequire__mutmut_3,
        "xǁEnvPrefixǁrequire__mutmut_4": xǁEnvPrefixǁrequire__mutmut_4,
        "xǁEnvPrefixǁrequire__mutmut_5": xǁEnvPrefixǁrequire__mutmut_5,
    }

    def require(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁrequire__mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁrequire__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    require.__signature__ = _mutmut_signature(xǁEnvPrefixǁrequire__mutmut_orig)
    xǁEnvPrefixǁrequire__mutmut_orig.__name__ = "xǁEnvPrefixǁrequire"

    def xǁEnvPrefixǁ__getitem____mutmut_orig(self, name: str) -> str | None:
        """Get environment variable using subscript notation."""
        return self.get_str(name)

    def xǁEnvPrefixǁ__getitem____mutmut_1(self, name: str) -> str | None:
        """Get environment variable using subscript notation."""
        return self.get_str(None)

    xǁEnvPrefixǁ__getitem____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁ__getitem____mutmut_1": xǁEnvPrefixǁ__getitem____mutmut_1
    }

    def __getitem__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁ__getitem____mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁ__getitem____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __getitem__.__signature__ = _mutmut_signature(xǁEnvPrefixǁ__getitem____mutmut_orig)
    xǁEnvPrefixǁ__getitem____mutmut_orig.__name__ = "xǁEnvPrefixǁ__getitem__"

    def xǁEnvPrefixǁ__contains____mutmut_orig(self, name: str) -> bool:
        """Check if environment variable exists."""
        return self._make_name(name) in os.environ

    def xǁEnvPrefixǁ__contains____mutmut_1(self, name: str) -> bool:
        """Check if environment variable exists."""
        return self._make_name(None) in os.environ

    def xǁEnvPrefixǁ__contains____mutmut_2(self, name: str) -> bool:
        """Check if environment variable exists."""
        return self._make_name(name) not in os.environ

    xǁEnvPrefixǁ__contains____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁ__contains____mutmut_1": xǁEnvPrefixǁ__contains____mutmut_1,
        "xǁEnvPrefixǁ__contains____mutmut_2": xǁEnvPrefixǁ__contains____mutmut_2,
    }

    def __contains__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁ__contains____mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁ__contains____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __contains__.__signature__ = _mutmut_signature(xǁEnvPrefixǁ__contains____mutmut_orig)
    xǁEnvPrefixǁ__contains____mutmut_orig.__name__ = "xǁEnvPrefixǁ__contains__"

    def xǁEnvPrefixǁall_with_prefix__mutmut_orig(self) -> dict[str, str]:
        """Get all environment variables with this prefix.

        Returns:
            Dictionary of variable names (without prefix) to values

        """
        result = {}
        prefix_with_sep = f"{self.prefix}{self.separator}"

        for key, value in os.environ.items():
            if key.startswith(prefix_with_sep):
                # Remove prefix and add to result
                var_name = key[len(prefix_with_sep) :]
                result[var_name] = value

        return result

    def xǁEnvPrefixǁall_with_prefix__mutmut_1(self) -> dict[str, str]:
        """Get all environment variables with this prefix.

        Returns:
            Dictionary of variable names (without prefix) to values

        """
        result = None
        prefix_with_sep = f"{self.prefix}{self.separator}"

        for key, value in os.environ.items():
            if key.startswith(prefix_with_sep):
                # Remove prefix and add to result
                var_name = key[len(prefix_with_sep) :]
                result[var_name] = value

        return result

    def xǁEnvPrefixǁall_with_prefix__mutmut_2(self) -> dict[str, str]:
        """Get all environment variables with this prefix.

        Returns:
            Dictionary of variable names (without prefix) to values

        """
        result = {}
        prefix_with_sep = None

        for key, value in os.environ.items():
            if key.startswith(prefix_with_sep):
                # Remove prefix and add to result
                var_name = key[len(prefix_with_sep) :]
                result[var_name] = value

        return result

    def xǁEnvPrefixǁall_with_prefix__mutmut_3(self) -> dict[str, str]:
        """Get all environment variables with this prefix.

        Returns:
            Dictionary of variable names (without prefix) to values

        """
        result = {}
        prefix_with_sep = f"{self.prefix}{self.separator}"

        for key, value in os.environ.items():
            if key.startswith(None):
                # Remove prefix and add to result
                var_name = key[len(prefix_with_sep) :]
                result[var_name] = value

        return result

    def xǁEnvPrefixǁall_with_prefix__mutmut_4(self) -> dict[str, str]:
        """Get all environment variables with this prefix.

        Returns:
            Dictionary of variable names (without prefix) to values

        """
        result = {}
        prefix_with_sep = f"{self.prefix}{self.separator}"

        for key, value in os.environ.items():
            if key.startswith(prefix_with_sep):
                # Remove prefix and add to result
                var_name = None
                result[var_name] = value

        return result

    def xǁEnvPrefixǁall_with_prefix__mutmut_5(self) -> dict[str, str]:
        """Get all environment variables with this prefix.

        Returns:
            Dictionary of variable names (without prefix) to values

        """
        result = {}
        prefix_with_sep = f"{self.prefix}{self.separator}"

        for key, value in os.environ.items():
            if key.startswith(prefix_with_sep):
                # Remove prefix and add to result
                var_name = key[len(prefix_with_sep) :]
                result[var_name] = None

        return result

    xǁEnvPrefixǁall_with_prefix__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEnvPrefixǁall_with_prefix__mutmut_1": xǁEnvPrefixǁall_with_prefix__mutmut_1,
        "xǁEnvPrefixǁall_with_prefix__mutmut_2": xǁEnvPrefixǁall_with_prefix__mutmut_2,
        "xǁEnvPrefixǁall_with_prefix__mutmut_3": xǁEnvPrefixǁall_with_prefix__mutmut_3,
        "xǁEnvPrefixǁall_with_prefix__mutmut_4": xǁEnvPrefixǁall_with_prefix__mutmut_4,
        "xǁEnvPrefixǁall_with_prefix__mutmut_5": xǁEnvPrefixǁall_with_prefix__mutmut_5,
    }

    def all_with_prefix(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEnvPrefixǁall_with_prefix__mutmut_orig"),
            object.__getattribute__(self, "xǁEnvPrefixǁall_with_prefix__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    all_with_prefix.__signature__ = _mutmut_signature(xǁEnvPrefixǁall_with_prefix__mutmut_orig)
    xǁEnvPrefixǁall_with_prefix__mutmut_orig.__name__ = "xǁEnvPrefixǁall_with_prefix"


# <3 🧱🤝🧰🪄
