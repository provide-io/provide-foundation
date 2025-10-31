#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

# Re-export cache utilities
from provide.foundation.serialization.cache import (
    CACHE_ENABLED,
    CACHE_SIZE,
    get_cache_key,
    serialization_cache,
)

# Re-export ENV format
from provide.foundation.serialization.env import env_dumps, env_loads

# Re-export INI format
from provide.foundation.serialization.ini import ini_dumps, ini_loads

# Re-export JSON format
from provide.foundation.serialization.json import json_dumps, json_loads

# Re-export TOML format
from provide.foundation.serialization.toml import toml_dumps, toml_loads

# Re-export YAML format
from provide.foundation.serialization.yaml import yaml_dumps, yaml_loads

"""Core serialization utilities for Foundation.

This module provides a unified interface for serialization operations
across multiple formats (JSON, YAML, TOML, INI, ENV) with optional
caching support for improved performance.

All serialization functions follow consistent patterns:
- _loads() functions deserialize strings to Python objects
- _dumps() functions serialize Python objects to strings
- Caching is configurable via environment variables
- Consistent error handling using ValidationError

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
