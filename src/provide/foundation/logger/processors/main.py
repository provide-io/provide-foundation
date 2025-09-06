#
# processors.py
#
"""
Structlog processors for Foundation Telemetry.
"""

import json
import logging as stdlib_logging
from typing import TYPE_CHECKING, Any, TextIO, cast

import structlog

from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
from provide.foundation.logger.custom_processors import (
    StructlogProcessor,
    add_log_level_custom,
    add_logger_name_emoji_prefix,
    filter_by_level_custom,
)

# Import trace context processor
from provide.foundation.logger.processors.trace import inject_trace_context
from provide.foundation.types import (
    TRACE_LEVEL_NUM,
    LogLevelStr,
)

if TYPE_CHECKING:
    from provide.foundation.logger.setup.emoji_resolver import ResolvedEmojiConfig

_LEVEL_TO_NUMERIC: dict[LogLevelStr, int] = {
    "CRITICAL": stdlib_logging.CRITICAL,
    "ERROR": stdlib_logging.ERROR,
    "WARNING": stdlib_logging.WARNING,
    "INFO": stdlib_logging.INFO,
    "DEBUG": stdlib_logging.DEBUG,
    "TRACE": TRACE_LEVEL_NUM,
    "NOTSET": stdlib_logging.NOTSET,
}


def _config_create_service_name_processor(
    service_name: str | None,
) -> StructlogProcessor:
    def processor(
        _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        if service_name is not None:
            event_dict["service_name"] = service_name
        return event_dict

    return cast(StructlogProcessor, processor)


def _config_create_timestamp_processors(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False)
    ]
    if omit_timestamp:

        def pop_timestamp_processor(
            _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None)
            return event_dict

        processors.append(cast(StructlogProcessor, pop_timestamp_processor))
    return processors


def _config_create_emoji_processors(
    logging_config: LoggingConfig, resolved_emoji_config: "ResolvedEmojiConfig"
) -> list[StructlogProcessor]:
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast(StructlogProcessor, add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:
        # FIX: Create the processor as a closure with the resolved config
        resolved_field_definitions, resolved_emoji_sets_lookup = resolved_emoji_config

        def add_das_emoji_prefix_closure(
            _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
        ) -> structlog.types.EventDict:
            # This inner function now has access to the resolved config from its closure scope
            from provide.foundation.logger.emoji.matrix import (
                PRIMARY_EMOJI,
                SECONDARY_EMOJI,
                TERTIARY_EMOJI,
            )

            final_das_prefix_parts: list[str] = []

            if resolved_field_definitions:  # New Layered Emoji System is active
                for field_def in resolved_field_definitions:
                    value_from_event = event_dict.get(field_def.log_key)
                    if value_from_event is not None and field_def.emoji_set_name:
                        event_dict.pop(field_def.log_key, None)
                        emoji_set = resolved_emoji_sets_lookup.get(
                            field_def.emoji_set_name
                        )
                        if emoji_set:
                            value_str_lower = str(value_from_event).lower()
                            specific_emoji = emoji_set.emojis.get(value_str_lower)
                            default_key = (
                                field_def.default_emoji_override_key
                                or emoji_set.default_emoji_key
                            )
                            default_emoji = emoji_set.emojis.get(default_key, "❓")
                            chosen_emoji = (
                                specific_emoji
                                if specific_emoji is not None
                                else default_emoji
                            )
                            final_das_prefix_parts.append(f"[{chosen_emoji}]")
                        else:
                            final_das_prefix_parts.append("[❓]")
            else:  # Fallback to Core DAS System
                domain = event_dict.pop("domain", None)
                action = event_dict.pop("action", None)
                status = event_dict.pop("status", None)
                if domain or action or status:
                    domain_emoji = (
                        PRIMARY_EMOJI.get(str(domain).lower(), PRIMARY_EMOJI["default"])
                        if domain
                        else PRIMARY_EMOJI["default"]
                    )
                    action_emoji = (
                        SECONDARY_EMOJI.get(
                            str(action).lower(), SECONDARY_EMOJI["default"]
                        )
                        if action
                        else SECONDARY_EMOJI["default"]
                    )
                    status_emoji = (
                        TERTIARY_EMOJI.get(
                            str(status).lower(), TERTIARY_EMOJI["default"]
                        )
                        if status
                        else TERTIARY_EMOJI["default"]
                    )
                    final_das_prefix_parts.extend(
                        [f"[{domain_emoji}]", f"[{action_emoji}]", f"[{status_emoji}]"]
                    )

            if final_das_prefix_parts:
                final_das_prefix_str = "".join(final_das_prefix_parts)
                event_msg = event_dict.get("event")
                event_dict["event"] = (
                    f"{final_das_prefix_str} {event_msg}"
                    if event_msg is not None
                    else final_das_prefix_str
                )
            return event_dict

        processors.append(cast(StructlogProcessor, add_das_emoji_prefix_closure))
    return processors


def _build_core_processors_list(
    config: TelemetryConfig, resolved_emoji_config: "ResolvedEmojiConfig"
) -> list[StructlogProcessor]:
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars,
        cast(StructlogProcessor, add_log_level_custom),
        cast(
            StructlogProcessor,
            filter_by_level_custom(
                default_level_str=log_cfg.default_level,
                module_levels=log_cfg.module_levels,
                level_to_numeric_map=_LEVEL_TO_NUMERIC,
            ),
        ),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
    ]

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
        processors.append(cast(StructlogProcessor, rate_limiter_processor))

    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add trace context injection if tracing is enabled
    if config.tracing_enabled and not config.globally_disabled:
        processors.append(cast(StructlogProcessor, inject_trace_context))

    processors.extend(_config_create_emoji_processors(log_cfg, resolved_emoji_config))
    return processors


def _config_create_json_formatter_processors() -> list[StructlogProcessor]:
    return [
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(serializer=json.dumps, sort_keys=False),
    ]


def _config_create_keyvalue_formatter_processors(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    def pop_logger_name_processor(
        _logger: object, _method_name: str, event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict

    is_tty = hasattr(output_stream, "isatty") and output_stream.isatty()
    return [
        cast(StructlogProcessor, pop_logger_name_processor),
        structlog.dev.ConsoleRenderer(
            colors=is_tty, exception_formatter=structlog.dev.plain_traceback
        ),
    ]


def _build_formatter_processors_list(
    logging_config: LoggingConfig, output_stream: TextIO
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
                create_core_setup_logger,
            )

            setup_logger = create_core_setup_logger()
            setup_logger.warning(
                f"Unknown formatter '{logging_config.console_formatter}', using default 'key_value'. "
                f"Valid formatters: ['json', 'key_value']"
            )
            return _config_create_keyvalue_formatter_processors(output_stream)
