# provide/foundation/serialization/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.serialization.core import (
    CACHE_ENABLED,
    CACHE_SIZE,
    env_dumps,
    env_loads,
    get_cache_key,
    ini_dumps,
    ini_loads,
    json_dumps,
    json_loads,
    serialization_cache,
    toml_dumps,
    toml_loads,
    yaml_dumps,
    yaml_loads,
)

"""Serialization utilities for Foundation.

Provides consistent serialization handling with validation,
caching support, and integration with Foundation's configuration system.

Supported Formats:
    - JSON: json_dumps(), json_loads()
    - YAML: yaml_dumps(), yaml_loads()
    - TOML: toml_dumps(), toml_loads()
    - INI: ini_dumps(), ini_loads()
    - ENV: env_dumps(), env_loads()

All _loads() functions support optional caching for improved performance
with frequently-accessed serialized data.

Environment Variables:
    FOUNDATION_SERIALIZATION_CACHE_ENABLED: Enable/disable caching (default: True)
    FOUNDATION_SERIALIZATION_CACHE_SIZE: Cache size limit (default: 128)
"""

__all__ = [
    # Cache utilities
    "CACHE_ENABLED",
    "CACHE_SIZE",
    # ENV
    "env_dumps",
    "env_loads",
    "get_cache_key",
    # INI
    "ini_dumps",
    "ini_loads",
    # JSON
    "json_dumps",
    "json_loads",
    "serialization_cache",
    # TOML
    "toml_dumps",
    "toml_loads",
    # YAML
    "yaml_dumps",
    "yaml_loads",
]
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


# <3 🧱🤝📜🪄
