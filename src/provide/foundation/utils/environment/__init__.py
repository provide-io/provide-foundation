#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

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
from provide.foundation.utils.environment.parsers import parse_duration, parse_size
from provide.foundation.utils.environment.prefix import EnvPrefix

"""Environment variable utilities with type coercion and prefix support.

Provides utilities for safely reading and parsing environment variables with
automatic type detection, prefix-based namespacing, and default value handling.
"""

__all__ = [
    "EnvPrefix",
    "get_bool",
    "get_dict",
    "get_float",
    "get_int",
    "get_list",
    "get_path",
    "get_str",
    "parse_duration",
    "parse_size",
    "require",
]

# 🧱🏗️🔚
