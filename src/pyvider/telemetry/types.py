# src/pyvider/telemetry/types.py
"""
Pyvider Telemetry Custom Type Definitions and Constants.

This module centralizes custom type aliases and constants used throughout the
`pyvider-telemetry` package. These definitions are crucial for:
- Configuration: Defining the allowed values for settings like log levels and
  formatter types (e.g., `LogLevelStr`, `ConsoleFormatterStr`).
- Type Safety: Ensuring that interactions with the library's API and internal
  components are type-checked, improving robustness and maintainability.
- Clarity: Providing clear, domain-specific names for common data structures
  or literal sets.

Key Definitions:
- `LogLevelStr`: A `typing.Literal` type for valid log level strings
  (e.g., "DEBUG", "INFO", "ERROR").
- `_VALID_LOG_LEVEL_TUPLE`: A tuple containing all valid `LogLevelStr` values,
  used for validation.
- `ConsoleFormatterStr`: A `typing.Literal` type for console formatter choices
  (e.g., "key_value", "json").
- `_VALID_FORMATTER_TUPLE`: A tuple of valid `ConsoleFormatterStr` values.
- TRACE Level Constants:
    - `TRACE_LEVEL_NUM`: The numeric value for the custom "TRACE" log level.
    - `TRACE_LEVEL_NAME`: The string name "TRACE".
  This module also includes logic to register this custom TRACE level with the
  standard `logging` module if it's not already present, including adding a
  `trace()` method to `logging.Logger`.

By consolidating these fundamental definitions here, we avoid circular dependencies
and provide a single source of truth for these important types and constants.
"""
import logging as stdlib_logging  # Moved to top
from typing import Literal

# Define fundamental type aliases for log levels
LogLevelStr = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", "NOTSET"]
"""Type alias for valid log level strings, ensuring type safety for configuration."""

_VALID_LOG_LEVEL_TUPLE: tuple[LogLevelStr, ...] = (
    "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", "NOTSET"
)
"""Tuple of all valid `LogLevelStr` values, used for runtime validation of log levels."""

# Define fundamental type aliases for console formatters
ConsoleFormatterStr = Literal["key_value", "json"]
"""Type alias for console formatter choices, restricting options to supported formats."""

_VALID_FORMATTER_TUPLE: tuple[ConsoleFormatterStr, ...] = ("key_value", "json")
"""Tuple of all valid `ConsoleFormatterStr` values, used for runtime validation of formatters."""

# Numeric representation of TRACE log level
TRACE_LEVEL_NUM: int = 5 # Typically, DEBUG is 10, so TRACE is lower
"""Numeric value for the custom TRACE log level."""

# Name for the TRACE log level
TRACE_LEVEL_NAME: str = "TRACE"
"""String name for the custom TRACE log level."""

# Add TRACE to standard library logging if it doesn't exist
if not hasattr(stdlib_logging, TRACE_LEVEL_NAME): # pragma: no cover
    stdlib_logging.addLevelName(TRACE_LEVEL_NUM, TRACE_LEVEL_NAME)

    # Define a trace method on the Logger class if it doesn't exist
    # This is to allow logger.trace("message")
    def trace(self: stdlib_logging.Logger, message: str, *args: object, **kwargs: object) -> None: # pragma: no cover
        if self.isEnabledFor(TRACE_LEVEL_NUM):
            self._log(TRACE_LEVEL_NUM, message, args, **kwargs) # type: ignore[arg-type]

    if not hasattr(stdlib_logging.Logger, "trace"): # pragma: no cover
        stdlib_logging.Logger.trace = trace # type: ignore[attr-defined]

    # Also add to the root logger if it's already instantiated
    if stdlib_logging.root and not hasattr(stdlib_logging.root, "trace"): # pragma: no cover
         stdlib_logging.root.trace = trace.__get__(stdlib_logging.root, stdlib_logging.Logger) # type: ignore[attr-defined]

    # And to the getLogger result (which might be a Logger or a PlaceHolder)
    # This is a bit more involved if we want to be absolutely sure,
    # but typically custom levels are added before loggers are widely obtained.
    # For structlog, this setup is more about making the level known to stdlib.
    # The actual handling of 'trace' method calls in structlog will be managed
    # by how structlog is configured to wrap stdlib loggers or by its own methods.
    # We also need to ensure structlog knows about this level if we use its level filtering.
    # This is handled by `_LEVEL_TO_NUMERIC` in config.py for structlog's custom filtering.
