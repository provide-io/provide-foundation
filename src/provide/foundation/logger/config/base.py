#
# base.py
#
"""
Base configuration utilities for Foundation logger.
"""

import os
import sys


def get_config_logger():
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

    return structlog.get_logger("provide.foundation.logger.config")
