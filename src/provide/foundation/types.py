"""
Core type definitions and constants for Foundation.

This module contains core logging-related types and constants
that are used across multiple modules in the foundation package.
"""

import logging as stdlib_logging
from typing import cast, Any, Literal

# --- Core Log Level and Formatter Types ---
LogLevelStr = Literal[
    "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", "NOTSET"
]
"""Type alias for valid log level strings, ensuring type safety for configuration."""

_VALID_LOG_LEVEL_TUPLE: tuple[LogLevelStr, ...] = (
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
    "TRACE",
    "NOTSET",
)
"""Tuple of all valid `LogLevelStr` values, used for runtime validation of log levels."""

ConsoleFormatterStr = Literal["key_value", "json"]
"""Type alias for console formatter choices, restricting options to supported formats."""

_VALID_FORMATTER_TUPLE: tuple[ConsoleFormatterStr, ...] = ("key_value", "json")
"""Tuple of all valid `ConsoleFormatterStr` values, used for runtime validation of formatters."""

# --- TRACE Level Constants ---
TRACE_LEVEL_NUM: int = 5  # Typically, DEBUG is 10, so TRACE is lower
"""Numeric value for the custom TRACE log level."""

TRACE_LEVEL_NAME: str = "TRACE"
"""String name for the custom TRACE log level."""

# Add TRACE to standard library logging if it doesn't exist
if not hasattr(stdlib_logging, TRACE_LEVEL_NAME):  # pragma: no cover
    stdlib_logging.addLevelName(TRACE_LEVEL_NUM, TRACE_LEVEL_NAME)

    def trace(
        self: stdlib_logging.Logger, message: str, *args: object, **kwargs: object
    ) -> None:  # pragma: no cover
        if self.isEnabledFor(TRACE_LEVEL_NUM):
            self._log(TRACE_LEVEL_NUM, message, args, **kwargs)  # type: ignore[arg-type]

    if not hasattr(stdlib_logging.Logger, "trace"):  # pragma: no cover
        stdlib_logging.Logger.trace = trace  # type: ignore[attr-defined]
    if stdlib_logging.root and not hasattr(
        stdlib_logging.root, "trace"
    ):  # pragma: no cover
        (cast(Any, stdlib_logging.root)).trace = trace.__get__(
            stdlib_logging.root, stdlib_logging.Logger
        )
