#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from provide.foundation.logger.config.logging import LoggingConfig

"""Logger defaults for Foundation configuration."""

# =================================
# Logging Defaults
# =================================
DEFAULT_LOG_LEVEL = "WARNING"
DEFAULT_CONSOLE_FORMATTER = "key_value"
DEFAULT_LOGGER_NAME_EMOJI_ENABLED = True
DEFAULT_DAS_EMOJI_ENABLED = True
DEFAULT_OMIT_TIMESTAMP = False
DEFAULT_FOUNDATION_SETUP_LOG_LEVEL = "WARNING"
DEFAULT_FOUNDATION_LOG_OUTPUT = "stderr"

# =================================
# Rate Limiting Defaults
# =================================
DEFAULT_RATE_LIMIT_ENABLED = False
DEFAULT_RATE_LIMIT_EMIT_WARNINGS = True
DEFAULT_RATE_LIMIT_GLOBAL = 5.0
DEFAULT_RATE_LIMIT_GLOBAL_CAPACITY = 1000
DEFAULT_RATE_LIMIT_OVERFLOW_POLICY = "drop_oldest"

# =================================
# Sanitization Defaults
# =================================
DEFAULT_SANITIZATION_ENABLED = True
DEFAULT_SANITIZATION_MASK_PATTERNS = True
DEFAULT_SANITIZATION_SANITIZE_DICTS = True

# =================================
# Logger System Defaults
# =================================
DEFAULT_FALLBACK_LOG_LEVEL = "INFO"
DEFAULT_FALLBACK_LOG_LEVEL_NUMERIC = 20

# =================================
# Factory Functions for Mutable Defaults
# =================================


def default_module_levels() -> dict[str, str]:
    """Factory for module log levels dictionary."""
    return {
        "asyncio": "INFO",  # Suppress asyncio DEBUG messages (e.g., selector events)
    }


def default_rate_limits() -> dict[str, tuple[float, float]]:
    """Factory for per-logger rate limits dictionary."""
    return {}


def default_logging_config() -> LoggingConfig:
    """Factory for LoggingConfig instance."""
    from provide.foundation.logger.config.logging import LoggingConfig

    return LoggingConfig.from_env()


__all__ = [
    "DEFAULT_CONSOLE_FORMATTER",
    "DEFAULT_DAS_EMOJI_ENABLED",
    "DEFAULT_FALLBACK_LOG_LEVEL",
    "DEFAULT_FALLBACK_LOG_LEVEL_NUMERIC",
    "DEFAULT_FOUNDATION_LOG_OUTPUT",
    "DEFAULT_FOUNDATION_SETUP_LOG_LEVEL",
    "DEFAULT_LOGGER_NAME_EMOJI_ENABLED",
    "DEFAULT_LOG_LEVEL",
    "DEFAULT_OMIT_TIMESTAMP",
    "DEFAULT_RATE_LIMIT_EMIT_WARNINGS",
    "DEFAULT_RATE_LIMIT_ENABLED",
    "DEFAULT_RATE_LIMIT_GLOBAL",
    "DEFAULT_RATE_LIMIT_GLOBAL_CAPACITY",
    "DEFAULT_RATE_LIMIT_OVERFLOW_POLICY",
    "DEFAULT_SANITIZATION_ENABLED",
    "DEFAULT_SANITIZATION_MASK_PATTERNS",
    "DEFAULT_SANITIZATION_SANITIZE_DICTS",
    "default_logging_config",
    "default_module_levels",
    "default_rate_limits",
]

# 🧱🏗️🔚
