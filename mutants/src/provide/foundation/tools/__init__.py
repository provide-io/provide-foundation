# provide/foundation/tools/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.tools.base import (
    BaseToolManager,
    ToolError,
    ToolMetadata,
)
from provide.foundation.tools.cache import ToolCache
from provide.foundation.tools.downloader import ToolDownloader
from provide.foundation.tools.installer import ToolInstaller
from provide.foundation.tools.registry import (
    get_tool_manager,
    get_tool_registry,
    register_tool_manager,
)
from provide.foundation.tools.resolver import VersionResolver

"""Provide Foundation Tools Module
================================

Unified tool management system for downloading, verifying, installing, and
managing development tools across the provide-io ecosystem.

This module provides:
- Base classes for tool managers
- Download orchestration with progress reporting
- Checksum and signature verification
- Installation handling for various formats
- Version resolution (latest, semver, wildcards)
- Caching with TTL support
- Tool registry integration

Example:
    >>> from provide.foundation.tools import get_tool_manager
    >>> from provide.foundation.config import BaseConfig
    >>>
    >>> config = BaseConfig()
    >>> tf_manager = get_tool_manager("terraform", config)
    >>> tf_manager.install("1.5.0")
    PosixPath('/home/user/.provide-foundation/tools/terraform/1.5.0')

"""

__all__ = [
    # Base classes
    "BaseToolManager",
    # Components
    "ToolCache",
    "ToolDownloader",
    "ToolError",
    "ToolInstaller",
    "ToolMetadata",
    "VersionResolver",
    # Registry functions
    "get_tool_manager",
    "get_tool_registry",
    "register_tool_manager",
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


# <3 🧱🤝🔧🪄
