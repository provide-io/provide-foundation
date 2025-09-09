#
# trace.py
#
"""
TRACE log level setup and patching.

This module handles the custom TRACE log level implementation,
including patching the standard library logging module.
"""

import logging as stdlib_logging
from typing import Any, cast

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

# Also patch PrintLogger from structlog to support trace method
try:
    import structlog
    from structlog import PrintLogger
    
    if not hasattr(PrintLogger, "trace"):  # pragma: no cover
        def trace_for_print_logger(
            self: PrintLogger, msg: object, *args: object, **kwargs: object
        ) -> None:  # pragma: no cover
            # PrintLogger doesn't have level checking, so just format and print like other methods
            if args:
                try:
                    formatted_msg = str(msg) % args
                except (TypeError, ValueError):
                    formatted_msg = f"{msg} {args}"
            else:
                formatted_msg = str(msg)
            
            # Use the same output mechanism as other PrintLogger methods
            self._file.write(formatted_msg + "\n")
            self._file.flush()
        
        PrintLogger.trace = trace_for_print_logger  # type: ignore[attr-defined]
        
except ImportError:  # pragma: no cover
    pass
