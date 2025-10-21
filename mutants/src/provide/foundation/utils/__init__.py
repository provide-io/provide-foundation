# provide/foundation/utils/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.parsers import (
    auto_parse,
    parse_bool,
    parse_dict,
    parse_list,
    parse_typed_value,
)
from provide.foundation.utils.deps import (
    DependencyStatus,
    check_optional_deps,
    get_available_features,
    get_optional_dependencies,
    has_dependency,
    require_dependency,
)
from provide.foundation.utils.environment import (
    EnvPrefix,
    get_bool,
    get_dict,
    get_float,
    get_int,
    get_list,
    get_path,
    get_str,
    parse_duration,
    parse_size,
    require,
)
from provide.foundation.utils.importer import lazy_import
from provide.foundation.utils.rate_limiting import TokenBucketRateLimiter
from provide.foundation.utils.scoped_cache import ContextScopedCache
from provide.foundation.utils.stubs import (
    create_dependency_stub,
    create_function_stub,
    create_module_stub,
)
from provide.foundation.utils.timing import timed_block
from provide.foundation.utils.versioning import get_version, reset_version_cache

"""Utility modules for provide.foundation.

Common utilities that can be used across the foundation and by other packages.
"""

__all__ = [
    # Caching utilities
    "ContextScopedCache",
    "DependencyStatus",
    "EnvPrefix",
    # Rate limiting utilities
    "TokenBucketRateLimiter",
    # Parsing utilities
    "auto_parse",
    # Dependency checking utilities
    "check_optional_deps",
    # Stub creation utilities
    "create_dependency_stub",
    "create_function_stub",
    "create_module_stub",
    # Module exports
    "environment",
    "get_available_features",
    # Environment utilities
    "get_bool",
    "get_dict",
    "get_float",
    "get_int",
    "get_list",
    "get_optional_dependencies",
    "get_path",
    "get_str",
    # Versioning utilities
    "get_version",
    "has_dependency",
    # Lazy import utilities
    "lazy_import",
    "parse_bool",
    "parse_dict",
    "parse_duration",
    "parse_list",
    "parse_size",
    "parse_typed_value",
    "require",
    "require_dependency",
    # Timing utilities
    "reset_version_cache",
    "timed_block",
]
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


def x___getattr____mutmut_orig(name: str) -> Any:
    """Lazy import for modules."""
    if name == "environment":
        from provide.foundation.utils import environment as env_module

        return env_module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def x___getattr____mutmut_1(name: str) -> Any:
    """Lazy import for modules."""
    if name != "environment":
        from provide.foundation.utils import environment as env_module

        return env_module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def x___getattr____mutmut_2(name: str) -> Any:
    """Lazy import for modules."""
    if name == "XXenvironmentXX":
        from provide.foundation.utils import environment as env_module

        return env_module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def x___getattr____mutmut_3(name: str) -> Any:
    """Lazy import for modules."""
    if name == "ENVIRONMENT":
        from provide.foundation.utils import environment as env_module

        return env_module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def x___getattr____mutmut_4(name: str) -> Any:
    """Lazy import for modules."""
    if name == "environment":
        from provide.foundation.utils import environment as env_module

        return env_module
    raise AttributeError(None)

x___getattr____mutmut_mutants : ClassVar[MutantDict] = {
'x___getattr____mutmut_1': x___getattr____mutmut_1, 
    'x___getattr____mutmut_2': x___getattr____mutmut_2, 
    'x___getattr____mutmut_3': x___getattr____mutmut_3, 
    'x___getattr____mutmut_4': x___getattr____mutmut_4
}

def __getattr__(*args, **kwargs):
    result = _mutmut_trampoline(x___getattr____mutmut_orig, x___getattr____mutmut_mutants, args, kwargs)
    return result 

__getattr__.__signature__ = _mutmut_signature(x___getattr____mutmut_orig)
x___getattr____mutmut_orig.__name__ = 'x___getattr__'


# <3 🧱🤝🧰🪄
