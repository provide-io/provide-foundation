from __future__ import annotations

from typing import Literal

from provide.foundation.logger.trace import TRACE_LEVEL_NAME, TRACE_LEVEL_NUM

"""Logger type definitions and constants."""

LogLevelStr = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", "NOTSET"]

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
    "LogLevelStr",
]
