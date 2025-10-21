# provide/foundation/platform/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.platform.detection import (
    PlatformError,
    get_arch_name,
    get_cpu_type,
    get_os_name,
    get_os_version,
    get_platform_string,
    normalize_platform_components,
)
from provide.foundation.platform.info import (
    SystemInfo,
    get_system_info,
    is_64bit,
    is_arm,
    is_linux,
    is_macos,
    is_windows,
)

"""Platform detection and information utilities.

Provides cross-platform detection and system information gathering.
"""

__all__ = [
    # Classes
    "PlatformError",
    "SystemInfo",
    # Detection functions
    "get_arch_name",
    "get_cpu_type",
    "get_os_name",
    "get_os_version",
    "get_platform_string",
    "get_system_info",
    # Platform checks
    "is_64bit",
    "is_arm",
    "is_linux",
    "is_macos",
    "is_windows",
    # Utilities
    "normalize_platform_components",
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


# <3 🧱🤝🏗️🪄
