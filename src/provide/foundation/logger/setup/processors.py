#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# processors.py
#
from typing import Any, TextIO, cast

import structlog

from provide.foundation.logger.config import TelemetryConfig
from provide.foundation.logger.processors import (
    _build_core_processors_list,
    _build_formatter_processors_list,
)

"""Processor chain building for Foundation Telemetry.
Handles the assembly of structlog processor chains including emoji processing.
"""


def build_complete_processor_chain(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> list[Any]:
    """Build the complete processor chain for structlog.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    Returns:
        List of processors for structlog

    """
    core_processors = _build_core_processors_list(config)
    formatter_processors = _build_formatter_processors_list(config.logging, log_stream)
    return cast("list[Any]", core_processors + formatter_processors)


def apply_structlog_configuration(processors: list[Any], log_stream: TextIO) -> None:
    """Apply the processor configuration to structlog.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=cast("type[structlog.types.BindableLogger]", structlog.BoundLogger),
        cache_logger_on_first_use=cache_loggers,
    )


def configure_structlog_output(
    config: TelemetryConfig,
    log_stream: TextIO,
) -> None:
    """Configure structlog with the complete output chain.

    Args:
        config: Telemetry configuration
        log_stream: Output stream for logging

    """
    processors = build_complete_processor_chain(config, log_stream)
    apply_structlog_configuration(processors, log_stream)


def handle_globally_disabled_setup() -> None:
    """Configure structlog for globally disabled telemetry (no-op mode)."""
    structlog.configure(
        processors=[],
        logger_factory=structlog.ReturnLoggerFactory(),
        cache_logger_on_first_use=True,
    )


# 🧱🏗️🔚
