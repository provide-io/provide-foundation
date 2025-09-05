#
# processors.py
#
"""
Processor chain building for Foundation Telemetry.
Handles the assembly of structlog processor chains including emoji processing.
"""

import sys
from typing import Any, TextIO, cast

import structlog

from provide.foundation.logger.config import TelemetryConfig
from provide.foundation.logger.processors import (
    _build_core_processors_list,
    _build_formatter_processors_list,
)
from provide.foundation.logger.setup.emoji_resolver import ResolvedEmojiConfig


class PrintLoggerWithTrace:
    """PrintLogger wrapper that supports trace method."""
    
    def __init__(self, file: TextIO):
        self._print_logger = structlog.PrintLoggerFactory()(file)
        self._file = file
    
    def trace(self, message: str) -> None:
        """Support trace level logging."""
        self._print_logger.debug(message)
    
    def __getattr__(self, name: str) -> Any:
        """Delegate all other methods to the wrapped PrintLogger."""
        return getattr(self._print_logger, name)


class PrintLoggerFactoryWithTrace:
    """Logger factory that creates PrintLoggerWithTrace instances."""
    
    def __init__(self, file: TextIO):
        self._file = file
    
    def __call__(self, *args: Any, **kwargs: Any) -> PrintLoggerWithTrace:
        """Create a new logger instance."""
        return PrintLoggerWithTrace(self._file)


def build_complete_processor_chain(
    config: TelemetryConfig, 
    resolved_emoji_config: ResolvedEmojiConfig,
    log_stream: TextIO
) -> list[Any]:
    """
    Build the complete processor chain for structlog.
    
    Args:
        config: Telemetry configuration
        resolved_emoji_config: Resolved emoji configuration
        log_stream: Output stream for logging
        
    Returns:
        List of processors for structlog
    """
    core_processors = _build_core_processors_list(config, resolved_emoji_config)
    formatter_processors = _build_formatter_processors_list(
        config.logging, log_stream
    )
    return cast(list[Any], core_processors + formatter_processors)


def apply_structlog_configuration(processors: list[Any], log_stream: TextIO) -> None:
    """
    Apply the processor configuration to structlog.
    
    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging
    """
    structlog.configure(
        processors=processors,
        logger_factory=PrintLoggerFactoryWithTrace(file=log_stream),
        wrapper_class=cast(type[structlog.types.BindableLogger], structlog.BoundLogger),
        cache_logger_on_first_use=True,
    )


def configure_structlog_output(
    config: TelemetryConfig, 
    resolved_emoji_config: ResolvedEmojiConfig,
    log_stream: TextIO
) -> None:
    """
    Configure structlog with the complete output chain.
    
    Args:
        config: Telemetry configuration
        resolved_emoji_config: Resolved emoji configuration
        log_stream: Output stream for logging
    """
    processors = build_complete_processor_chain(config, resolved_emoji_config, log_stream)
    apply_structlog_configuration(processors, log_stream)


def handle_globally_disabled_setup() -> None:
    """
    Configure structlog for globally disabled telemetry (no-op mode).
    """
    structlog.configure(
        processors=[],
        logger_factory=structlog.ReturnLoggerFactory(),
        cache_logger_on_first_use=True,
    )