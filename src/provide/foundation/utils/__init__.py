#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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


def __getattr__(name: str) -> Any:
    """Lazy import for modules."""
    if name == "environment":
        from provide.foundation.utils import environment as env_module

        return env_module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# 🧱🏗️🔚
