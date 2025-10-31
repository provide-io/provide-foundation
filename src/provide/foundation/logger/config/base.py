#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# base.py
#
import os
import sys
from typing import Any

"""Base configuration utilities for Foundation logger."""


def get_config_logger() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.utils.streams import get_foundation_log_stream

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        output_stream = sys.stderr

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [structlog.dev.ConsoleRenderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


# 🧱🏗️🔚
