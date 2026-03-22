#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


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

_TRACE_LEVEL: int = 5


_DEBUG_LEVEL: int = 10


def _make_filtering_bound_logger_with_trace(level: int) -> type:
    """Create a FilteringBoundLogger class with Foundation extensions.

    ``structlog.make_filtering_bound_logger`` only creates methods for standard
    log levels (debug, info, warning, error, critical).  Foundation adds:

    - ``.trace()`` — custom TRACE level (5) via ``msg()`` + level hint
    - ``.is_debug_enabled()`` / ``.is_trace_enabled()`` — level-check helpers
      that callers use to guard expensive argument construction
    """
    # structlog only knows standard levels (10+).  TRACE (5) is Foundation's
    # custom level routed through msg(), so clamp to DEBUG for structlog.
    structlog_level = max(level, _DEBUG_LEVEL)
    cls = structlog.make_filtering_bound_logger(structlog_level)

    # --- Permissive no-op ---
    # structlog's _nop requires a positional `event` arg, but Foundation
    # callers sometimes pass only kwargs: ``log.debug(command="x")``.
    # Replace all nop methods with a permissive version.
    _standard_levels = {"debug": 10, "info": 20, "warning": 30, "error": 40, "critical": 50}

    def _permissive_nop(*_args: Any, **_kw: Any) -> None:
        return None

    for method_name, method_level in _standard_levels.items():
        if method_level < level:
            setattr(cls, method_name, _permissive_nop)

    # --- .trace() ---
    if level <= _TRACE_LEVEL:

        def _trace(self: Any, event: Any, *args: Any, **kw: Any) -> Any:
            kw["_foundation_level_hint"] = "trace"
            return self.msg(event, *args, **kw)

        cls.trace = _trace  # type: ignore[attr-defined]
    else:
        cls.trace = _permissive_nop  # type: ignore[attr-defined]

    # --- .is_debug_enabled() / .is_trace_enabled() ---
    # Baked in at class-creation time — zero overhead bool returns.
    _debug_ok = level <= _DEBUG_LEVEL
    _trace_ok = level <= _TRACE_LEVEL

    cls.is_debug_enabled = lambda self: _debug_ok  # type: ignore[attr-defined]
    cls.is_trace_enabled = lambda self: _trace_ok  # type: ignore[attr-defined]

    return cls


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


def apply_structlog_configuration(
    processors: list[Any], log_stream: TextIO, effective_level: int = 20
) -> None:
    """Apply the processor configuration to structlog.

    Uses ``structlog.make_filtering_bound_logger`` so that methods below
    *effective_level* are literal ``return None`` — zero overhead, no
    processor entry, no f-string evaluation needed.

    Args:
        processors: List of processors to configure
        log_stream: Output stream for logging
        effective_level: Numeric log level threshold (default 20 / INFO)

    """
    # Check if force stream redirect is enabled (for testing)
    # Disable caching to allow stream redirection to work properly
    from provide.foundation.streams.config import get_stream_config

    stream_config = get_stream_config()
    cache_loggers = not stream_config.force_stream_redirect

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=log_stream),
        wrapper_class=_make_filtering_bound_logger_with_trace(effective_level),
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
    from provide.foundation.logger.constants import LEVEL_TO_NUMERIC

    processors = build_complete_processor_chain(config, log_stream)
    effective_level = LEVEL_TO_NUMERIC.get(config.logging.default_level, 20)

    # FilteringBoundLogger must use the minimum of all configured levels so
    # module-level overrides (e.g. auth=DEBUG when default=INFO) can reach
    # the _LevelFilter processor which evaluates per-module thresholds.
    if config.logging.module_levels:
        for module_level_str in config.logging.module_levels.values():
            module_numeric = LEVEL_TO_NUMERIC.get(module_level_str, 20)
            if module_numeric < effective_level:
                effective_level = module_numeric

    apply_structlog_configuration(processors, log_stream, effective_level)


def handle_globally_disabled_setup() -> None:
    """Configure structlog for globally disabled telemetry (no-op mode).

    Uses a null logger factory that drops all output. The processor chain
    must still strip Foundation-specific context to avoid errors.
    """

    class NullLogger:
        """Logger that silently drops all output."""

        def msg(self, message: str) -> None:
            """Drop the message."""

        def __getattr__(self, name: str) -> Any:
            """Return self for any attribute access (debug, info, etc.)."""
            return self.msg

    class NullLoggerFactory:
        """Factory that returns NullLogger instances."""

        def __call__(self, *args: Any, **kwargs: Any) -> NullLogger:
            return NullLogger()

    def strip_foundation_context(
        _logger: Any,
        _method_name: str,
        event_dict: dict[str, object],
    ) -> dict[str, object]:
        """Strip Foundation-specific bound context before rendering."""
        event_dict.pop("logger_name", None)
        event_dict.pop("_foundation_level_hint", None)
        return event_dict

    structlog.configure(
        processors=[
            strip_foundation_context,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.BoundLogger,
        logger_factory=NullLoggerFactory(),
        cache_logger_on_first_use=True,
    )


# 🧱🏗️🔚
