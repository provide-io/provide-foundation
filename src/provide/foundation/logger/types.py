# provide/foundation/logger/types.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Literal, TypeAlias

from provide.foundation.logger.trace import TRACE_LEVEL_NAME, TRACE_LEVEL_NUM

"""Logger type definitions and constants."""

LogLevelStr = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", "NOTSET"]

# Common type aliases for logger-related data structures
ContextDict: TypeAlias = dict[str, Any]
LoggerMetadata: TypeAlias = dict[str, Any]
LogRecord: TypeAlias = dict[str, Any]

_VALID_LOG_LEVEL_TUPLE: tuple[LogLevelStr, ...] = (
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
    "TRACE",
    "NOTSET",
)

ConsoleFormatterStr = Literal["key_value", "json"]

_VALID_FORMATTER_TUPLE: tuple[ConsoleFormatterStr, ...] = ("key_value", "json")

__all__ = [
    "TRACE_LEVEL_NAME",
    "TRACE_LEVEL_NUM",
    "ConsoleFormatterStr",
    "ContextDict",
    "LogLevelStr",
    "LogRecord",
    "LoggerMetadata",
]


# <3 🧱🤝📝🪄
