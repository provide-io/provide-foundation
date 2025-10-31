#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import logging as stdlib_logging

from provide.foundation.logger.trace import TRACE_LEVEL_NUM
from provide.foundation.logger.types import LogLevelStr

"""Centralized constants for Foundation logger system.

All logger-related constants and numeric mappings are defined here
to provide a single source of truth and eliminate inline defaults.
"""

CRITICAL_LEVEL = stdlib_logging.CRITICAL  # 50
ERROR_LEVEL = stdlib_logging.ERROR  # 40
WARNING_LEVEL = stdlib_logging.WARNING  # 30
INFO_LEVEL = stdlib_logging.INFO  # 20
DEBUG_LEVEL = stdlib_logging.DEBUG  # 10
TRACE_LEVEL = TRACE_LEVEL_NUM  # 5
NOTSET_LEVEL = stdlib_logging.NOTSET  # 0

# =================================
# Level Name to Numeric Mapping
# =================================

LEVEL_TO_NUMERIC: dict[LogLevelStr, int] = {
    "CRITICAL": CRITICAL_LEVEL,
    "ERROR": ERROR_LEVEL,
    "WARNING": WARNING_LEVEL,
    "INFO": INFO_LEVEL,
    "DEBUG": DEBUG_LEVEL,
    "TRACE": TRACE_LEVEL,
    "NOTSET": NOTSET_LEVEL,
}

# =================================
# Default Fallback Constants
# =================================

DEFAULT_FALLBACK_LEVEL = "INFO"
DEFAULT_FALLBACK_NUMERIC = INFO_LEVEL

# =================================
# Valid Level Names (for validation)
# =================================

VALID_LEVEL_NAMES = frozenset(LEVEL_TO_NUMERIC.keys())

__all__ = [
    "CRITICAL_LEVEL",
    "DEBUG_LEVEL",
    "DEFAULT_FALLBACK_LEVEL",
    "DEFAULT_FALLBACK_NUMERIC",
    "ERROR_LEVEL",
    "INFO_LEVEL",
    "LEVEL_TO_NUMERIC",
    "NOTSET_LEVEL",
    "TRACE_LEVEL",
    "VALID_LEVEL_NAMES",
    "WARNING_LEVEL",
]

# 🧱🏗️🔚
