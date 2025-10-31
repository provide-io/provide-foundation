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

from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
from provide.foundation.logger.constants import LEVEL_TO_NUMERIC
from provide.foundation.logger.custom_processors import (
    StructlogProcessor,
    add_log_level_custom,
    add_logger_name_emoji_prefix,
    filter_by_level_custom,
)
from provide.foundation.logger.processors.trace import inject_trace_context
from provide.foundation.serialization import json_dumps

"""Structlog processors for Foundation Telemetry."""

# Module-level flags to prevent event enrichment re-initialization during resets
# These persist across structlog.reset_defaults() calls
_event_enrichment_initialized = False
_reset_in_progress = False


def _config_create_service_name_processor(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["service_name"] = service_name
        return event_dict

    return cast("StructlogProcessor", processor)


def _config_create_timestamp_processors(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast("StructlogProcessor", pop_timestamp_processor))
    return processors


def _config_create_event_enrichment_processors(
    logging_config: LoggingConfig,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast("StructlogProcessor", add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:

        def add_event_enrichment_processor(
            _logger: Any,
            _method_name: str,
            event_dict: structlog.types.EventDict,
        ) -> structlog.types.EventDict:
            # Skip event enrichment entirely during resets to prevent re-initialization
            global _reset_in_progress
            if _reset_in_progress:
                return event_dict

            # Lazy import to avoid circular dependency
            from provide.foundation.eventsets.registry import discover_event_sets
            from provide.foundation.eventsets.resolver import get_resolver

            # Use module-level flag to prevent re-initialization during resets
            global _event_enrichment_initialized
            if not _event_enrichment_initialized:
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )

                setup_logger = create_foundation_internal_logger()
                setup_logger.trace("Initializing event enrichment processor")
                discover_event_sets()
                _event_enrichment_initialized = True
                setup_logger.trace("Event enrichment processor initialized")

            resolver = get_resolver()
            return resolver.enrich_event(event_dict)

        processors.append(cast("StructlogProcessor", add_event_enrichment_processor))
    return processors


def set_reset_in_progress(in_progress: bool) -> None:
    """Set whether a reset is currently in progress.

    This prevents event enrichment from triggering during resets.
    """
    global _reset_in_progress
    _reset_in_progress = in_progress


def reset_event_enrichment_state() -> None:
    """Reset event enrichment initialization state for testing.

    This should only be called during test cleanup to allow re-initialization
    in the next test.
    """
    global _event_enrichment_initialized
    _event_enrichment_initialized = False


def _build_core_processors_list(config: TelemetryConfig) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast("StructlogProcessor", add_log_level_custom),
    ]

    # Add timestamps, service name, and trace context early
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast("StructlogProcessor", inject_trace_context))

    # Add sanitization processor early to sanitize all logged data
    if log_cfg.sanitization_enabled:
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        sanitization_processor = create_sanitization_processor(
            enabled=log_cfg.sanitization_enabled,
            mask_patterns=log_cfg.sanitization_mask_patterns,
            sanitize_dicts=log_cfg.sanitization_sanitize_dicts,
        )
        processors.append(cast("StructlogProcessor", sanitization_processor))

    # Add event enrichment (emojis) BEFORE OTLP so enriched logs are exported
    processors.extend(_config_create_event_enrichment_processors(log_cfg))

    # Add OTLP processor AFTER enrichment but BEFORE level filtering
    # This ensures emoji-enriched logs are sent to OpenTelemetry/OpenObserve for ALL log levels
    if config.otlp_endpoint:
        from provide.foundation.logger.processors.otlp import create_otlp_processor

        otlp_processor = create_otlp_processor(config)
        if otlp_processor is not None:
            processors.append(cast("StructlogProcessor", otlp_processor))

    # Add level filter for console output (this doesn't affect OTLP which already processed logs)
    processors.append(
        cast(
            "StructlogProcessor",
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=LEVEL_TO_NUMERIC,
            ),
        )
    )

    processors.extend(
        [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
        ]
    )

    # Add rate limiting processor if enabled
    if log_cfg.rate_limit_enabled:
        from provide.foundation.logger.ratelimit import create_rate_limiter_processor

        rate_limiter_processor = create_rate_limiter_processor(
            global_rate=log_cfg.rate_limit_global,
            global_capacity=log_cfg.rate_limit_global_capacity,
            per_logger_rates=log_cfg.rate_limit_per_logger,
            emit_warnings=log_cfg.rate_limit_emit_warnings,
            summary_interval=log_cfg.rate_limit_summary_interval,
            max_queue_size=log_cfg.rate_limit_max_queue_size,
            max_memory_mb=log_cfg.rate_limit_max_memory_mb,
            overflow_policy=log_cfg.rate_limit_overflow_policy,
        )
        processors.append(cast("StructlogProcessor", rate_limiter_processor))

    return processors


def _config_create_json_formatter_processors() -> list[StructlogProcessor]:
    return [
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(serializer=json_dumps, sort_keys=False),
    ]


def _config_create_keyvalue_formatter_processors(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast("StructlogProcessor", pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
    ]


def _build_formatter_processors_list(
    logging_config: LoggingConfig,
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    match logging_config.console_formatter:
        case "json":
            return _config_create_json_formatter_processors()
        case "key_value":
            return _config_create_keyvalue_formatter_processors(output_stream)
        case _:
            # Unknown formatter, warn and default to key_value
            # Use setup coordinator logger
            from provide.foundation.logger.setup.coordinator import (
                create_foundation_internal_logger,
            )

            setup_logger = create_foundation_internal_logger()
            setup_logger.warning(
                f"Unknown formatter '{logging_config.console_formatter}', using default 'key_value'. "
                f"Valid formatters: ['json', 'key_value']",
            )
            return _config_create_keyvalue_formatter_processors(output_stream)


# 🧱🏗️🔚
