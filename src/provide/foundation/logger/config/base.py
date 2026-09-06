#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

#
# base.py
#
import os
from typing import Any

"""Base configuration utilities for Foundation logger."""


def get_config_logger() -> Any:
    """Get logger for config warnings that respects FOUNDATION_LOG_OUTPUT."""
    import structlog

    from provide.foundation.logger.defaults import safe_console_renderer
    from provide.foundation.utils.streams import get_foundation_log_stream, get_safe_stderr

    try:
        foundation_output = os.getenv("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        output_stream = get_foundation_log_stream(foundation_output)
    except Exception:
        # get_safe_stderr, not sys.stderr: this logger carries emoji like every
        # other, and a raw cp1252 console stream raises UnicodeEncodeError on
        # the first line. This branch runs when stream selection has already
        # failed, so it is the one that can least afford to raise again.
        output_stream = get_safe_stderr()

    try:
        config = structlog.get_config()
        structlog.configure(
            processors=config.get("processors", [safe_console_renderer()]),
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=config.get("wrapper_class", structlog.BoundLogger),
            cache_logger_on_first_use=config.get("cache_logger_on_first_use", True),
        )
    except Exception:
        structlog.configure(
            processors=[safe_console_renderer()],
            logger_factory=structlog.PrintLoggerFactory(file=output_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger().bind(logger_name="provide.foundation.logger.config")


# 🧱🏗️🔚
