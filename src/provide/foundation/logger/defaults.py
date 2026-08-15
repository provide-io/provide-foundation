#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from typing import TYPE_CHECKING

import structlog

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


def safe_console_renderer(**kwargs: object) -> structlog.dev.ConsoleRenderer:
    """Factory for a ConsoleRenderer that never leaks stack-frame locals.

    structlog's built-in default `exception_formatter` is
    `RichTracebackFormatter(show_locals=True)`, which renders local variables
    from every frame in a traceback. Any `logger.error(..., exc_info=True)`
    call on an exception whose locals (or a caller's locals further up the
    stack) hold sensitive values will leak them into the rendered output.
    This factory pins `exception_formatter` to `structlog.dev.plain_traceback`
    unless the caller explicitly passes their own.
    """
    kwargs.setdefault("exception_formatter", structlog.dev.plain_traceback)
    return structlog.dev.ConsoleRenderer(**kwargs)


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
    "safe_console_renderer",
]

# 🧱🏗️🔚
