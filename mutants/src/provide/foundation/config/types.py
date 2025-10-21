# provide/foundation/config/types.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Type definitions for the configuration system."""

from __future__ import annotations

from enum import Enum
from typing import Any, TypeAlias

# Basic type aliases
ConfigValue = str | int | float | bool | None | list[Any] | dict[str, Any]
ConfigDict = dict[str, ConfigValue]

# Common configuration type aliases
HeaderDict: TypeAlias = dict[str, str]
EnvDict: TypeAlias = dict[str, str]
FieldMetadata: TypeAlias = dict[str, Any]
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


class ConfigSource(Enum):
    """Sources for configuration values with precedence order."""

    DEFAULT = 0  # Lowest precedence
    FILE = 10
    ENV = 20
    RUNTIME = 30  # Highest precedence

    def xǁConfigSourceǁ__lt____mutmut_orig(self, other: object) -> bool:
        """Enable comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value < other.value

    def xǁConfigSourceǁ__lt____mutmut_1(self, other: object) -> bool:
        """Enable comparison for precedence."""
        if isinstance(other, ConfigSource):
            return NotImplemented
        return self.value < other.value

    def xǁConfigSourceǁ__lt____mutmut_2(self, other: object) -> bool:
        """Enable comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value <= other.value
    
    xǁConfigSourceǁ__lt____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConfigSourceǁ__lt____mutmut_1': xǁConfigSourceǁ__lt____mutmut_1, 
        'xǁConfigSourceǁ__lt____mutmut_2': xǁConfigSourceǁ__lt____mutmut_2
    }
    
    def __lt__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConfigSourceǁ__lt____mutmut_orig"), object.__getattribute__(self, "xǁConfigSourceǁ__lt____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __lt__.__signature__ = _mutmut_signature(xǁConfigSourceǁ__lt____mutmut_orig)
    xǁConfigSourceǁ__lt____mutmut_orig.__name__ = 'xǁConfigSourceǁ__lt__'

    def xǁConfigSourceǁ__le____mutmut_orig(self, other: object) -> bool:
        """Enable <= comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value <= other.value

    def xǁConfigSourceǁ__le____mutmut_1(self, other: object) -> bool:
        """Enable <= comparison for precedence."""
        if isinstance(other, ConfigSource):
            return NotImplemented
        return self.value <= other.value

    def xǁConfigSourceǁ__le____mutmut_2(self, other: object) -> bool:
        """Enable <= comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value < other.value
    
    xǁConfigSourceǁ__le____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConfigSourceǁ__le____mutmut_1': xǁConfigSourceǁ__le____mutmut_1, 
        'xǁConfigSourceǁ__le____mutmut_2': xǁConfigSourceǁ__le____mutmut_2
    }
    
    def __le__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConfigSourceǁ__le____mutmut_orig"), object.__getattribute__(self, "xǁConfigSourceǁ__le____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __le__.__signature__ = _mutmut_signature(xǁConfigSourceǁ__le____mutmut_orig)
    xǁConfigSourceǁ__le____mutmut_orig.__name__ = 'xǁConfigSourceǁ__le__'

    def xǁConfigSourceǁ__gt____mutmut_orig(self, other: object) -> bool:
        """Enable > comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value > other.value

    def xǁConfigSourceǁ__gt____mutmut_1(self, other: object) -> bool:
        """Enable > comparison for precedence."""
        if isinstance(other, ConfigSource):
            return NotImplemented
        return self.value > other.value

    def xǁConfigSourceǁ__gt____mutmut_2(self, other: object) -> bool:
        """Enable > comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value >= other.value
    
    xǁConfigSourceǁ__gt____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConfigSourceǁ__gt____mutmut_1': xǁConfigSourceǁ__gt____mutmut_1, 
        'xǁConfigSourceǁ__gt____mutmut_2': xǁConfigSourceǁ__gt____mutmut_2
    }
    
    def __gt__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConfigSourceǁ__gt____mutmut_orig"), object.__getattribute__(self, "xǁConfigSourceǁ__gt____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __gt__.__signature__ = _mutmut_signature(xǁConfigSourceǁ__gt____mutmut_orig)
    xǁConfigSourceǁ__gt____mutmut_orig.__name__ = 'xǁConfigSourceǁ__gt__'

    def xǁConfigSourceǁ__ge____mutmut_orig(self, other: object) -> bool:
        """Enable >= comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value >= other.value

    def xǁConfigSourceǁ__ge____mutmut_1(self, other: object) -> bool:
        """Enable >= comparison for precedence."""
        if isinstance(other, ConfigSource):
            return NotImplemented
        return self.value >= other.value

    def xǁConfigSourceǁ__ge____mutmut_2(self, other: object) -> bool:
        """Enable >= comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value > other.value
    
    xǁConfigSourceǁ__ge____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConfigSourceǁ__ge____mutmut_1': xǁConfigSourceǁ__ge____mutmut_1, 
        'xǁConfigSourceǁ__ge____mutmut_2': xǁConfigSourceǁ__ge____mutmut_2
    }
    
    def __ge__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConfigSourceǁ__ge____mutmut_orig"), object.__getattribute__(self, "xǁConfigSourceǁ__ge____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __ge__.__signature__ = _mutmut_signature(xǁConfigSourceǁ__ge____mutmut_orig)
    xǁConfigSourceǁ__ge____mutmut_orig.__name__ = 'xǁConfigSourceǁ__ge__'

    def xǁConfigSourceǁ__eq____mutmut_orig(self, other: object) -> bool:
        """Enable == comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value == other.value

    def xǁConfigSourceǁ__eq____mutmut_1(self, other: object) -> bool:
        """Enable == comparison for precedence."""
        if isinstance(other, ConfigSource):
            return NotImplemented
        return self.value == other.value

    def xǁConfigSourceǁ__eq____mutmut_2(self, other: object) -> bool:
        """Enable == comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value != other.value
    
    xǁConfigSourceǁ__eq____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConfigSourceǁ__eq____mutmut_1': xǁConfigSourceǁ__eq____mutmut_1, 
        'xǁConfigSourceǁ__eq____mutmut_2': xǁConfigSourceǁ__eq____mutmut_2
    }
    
    def __eq__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConfigSourceǁ__eq____mutmut_orig"), object.__getattribute__(self, "xǁConfigSourceǁ__eq____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __eq__.__signature__ = _mutmut_signature(xǁConfigSourceǁ__eq____mutmut_orig)
    xǁConfigSourceǁ__eq____mutmut_orig.__name__ = 'xǁConfigSourceǁ__eq__'


class ConfigFormat(Enum):
    """Supported configuration file formats."""

    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    INI = "ini"
    ENV = "env"  # .env files

    @classmethod
    def from_extension(cls, filename: str) -> ConfigFormat | None:
        """Determine format from file extension."""
        ext_map = {
            ".json": cls.JSON,
            ".yaml": cls.YAML,
            ".yml": cls.YAML,
            ".toml": cls.TOML,
            ".ini": cls.INI,
            ".env": cls.ENV,
        }

        for ext, format_type in ext_map.items():
            if filename.lower().endswith(ext):
                return format_type
        return None


# <3 🧱🤝⚙️🪄
