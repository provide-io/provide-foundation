#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import logging as stdlib_logging
from typing import Any

"""Wrapper for stdlib logger to accept structlog-style kwargs."""


class StructuredStdlibLogger:
    """Wrapper around stdlib logger that accepts structlog-style kwargs."""

    def __init__(self, logger: Any) -> None:
        """Initialize with a stdlib logger instance."""
        self._logger = logger

    def _log(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at DEBUG level with structured kwargs."""
        self._log(stdlib_logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at INFO level with structured kwargs."""
        self._log(stdlib_logging.INFO, msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at WARNING level with structured kwargs."""
        self._log(stdlib_logging.WARNING, msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at ERROR level with structured kwargs."""
        self._log(stdlib_logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at CRITICAL level with structured kwargs."""
        self._log(stdlib_logging.CRITICAL, msg, *args, **kwargs)


__all__ = ["StructuredStdlibLogger"]

# 🧱🏗️🔚
