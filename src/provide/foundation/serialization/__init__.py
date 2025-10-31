#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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

# 🧱🏗️🔚
