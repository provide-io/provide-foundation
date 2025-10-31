#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from pathlib import Path

"""Centralized default values for Foundation configuration.
All defaults are defined here instead of inline in field definitions.
"""

# =================================
# Context Defaults
# =================================
DEFAULT_CONTEXT_LOG_LEVEL = "INFO"
DEFAULT_CONTEXT_PROFILE = "default"
DEFAULT_CONTEXT_DEBUG = False
DEFAULT_CONTEXT_JSON_OUTPUT = False
DEFAULT_CONTEXT_CONFIG_FILE = None
DEFAULT_CONTEXT_LOG_FILE = None
DEFAULT_CONTEXT_LOG_FORMAT = "key_value"
DEFAULT_CONTEXT_NO_COLOR = False
DEFAULT_CONTEXT_NO_EMOJI = False

# =================================
# Exit codes
# =================================
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_SIGINT = 130  # Standard exit code for SIGINT

# =================================
# Testing defaults
# =================================
DEFAULT_TEST_WAIT_TIMEOUT = 5.0
DEFAULT_TEST_PARALLEL_TIMEOUT = 10.0
DEFAULT_TEST_CHECKPOINT_TIMEOUT = 5.0

# =================================
# File/Lock defaults
# =================================
DEFAULT_FILE_LOCK_TIMEOUT = 10.0

# =================================
# File operation defaults
# =================================
DEFAULT_FILE_OP_IS_ATOMIC = False
DEFAULT_FILE_OP_IS_SAFE = True
DEFAULT_FILE_OP_HAS_BACKUP = False

# =================================
# Temporary file/directory defaults
# =================================
DEFAULT_TEMP_PREFIX = "provide_"
DEFAULT_TEMP_SUFFIX = ""
DEFAULT_TEMP_CLEANUP = True
DEFAULT_TEMP_TEXT_MODE = False

# =================================
# Directory operation defaults
# =================================
DEFAULT_DIR_MODE = 0o755
DEFAULT_DIR_PARENTS = True
DEFAULT_MISSING_OK = True

# =================================
# Atomic write defaults
# =================================
DEFAULT_ATOMIC_MODE = 0o644
DEFAULT_ATOMIC_ENCODING = "utf-8"

# =================================
# EventSet defaults
# =================================
DEFAULT_EVENT_KEY = "default"

# =================================
# Component defaults
# =================================
DEFAULT_COMPONENT_DIMENSION = "component"

# =================================
# State config defaults
# =================================
DEFAULT_STATE_CONFIG_NAME = ""

# =================================
# Tracer defaults
# =================================
DEFAULT_TRACER_OTEL_SPAN = None
DEFAULT_TRACER_ACTIVE = True

# =================================
# Factory functions for mutable defaults
# =================================


def default_empty_dict() -> dict[str, str]:
    """Factory for empty string dictionaries."""
    return {}


def path_converter(x: str | None) -> Path | None:
    """Convert string to Path or None."""
    return Path(x) if x else None


# 🧱🏗️🔚
