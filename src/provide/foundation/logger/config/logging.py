#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

# ruff: noqa: RUF009
from pathlib import Path

from attrs import define

from provide.foundation.config.base import field
from provide.foundation.config.converters import (
    parse_bool_extended,
    parse_console_formatter,
    parse_float_with_validation,
    parse_foundation_log_output,
    parse_log_level,
    parse_module_levels,
    parse_rate_limits,
    validate_log_level,
    validate_overflow_policy,
    validate_positive,
)
from provide.foundation.config.defaults import path_converter
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.logger.defaults import (
    DEFAULT_CONSOLE_FORMATTER,
    DEFAULT_DAS_EMOJI_ENABLED,
    DEFAULT_FOUNDATION_LOG_OUTPUT,
    DEFAULT_FOUNDATION_SETUP_LOG_LEVEL,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOGGER_NAME_EMOJI_ENABLED,
    DEFAULT_OMIT_TIMESTAMP,
    DEFAULT_RATE_LIMIT_EMIT_WARNINGS,
    DEFAULT_RATE_LIMIT_ENABLED,
    DEFAULT_RATE_LIMIT_GLOBAL,
    DEFAULT_RATE_LIMIT_GLOBAL_CAPACITY,
    DEFAULT_RATE_LIMIT_OVERFLOW_POLICY,
    DEFAULT_SANITIZATION_ENABLED,
    DEFAULT_SANITIZATION_MASK_PATTERNS,
    DEFAULT_SANITIZATION_SANITIZE_DICTS,
    default_module_levels,
    default_rate_limits,
)
from provide.foundation.logger.types import (
    ConsoleFormatterStr,
    LogLevelStr,
)

"""LoggingConfig class for Foundation logger configuration."""


@define(slots=True, repr=False)
class LoggingConfig(RuntimeConfig):
    """Configuration specific to logging behavior within Foundation Telemetry."""

    default_level: LogLevelStr = field(
        default=DEFAULT_LOG_LEVEL,
        env_var="PROVIDE_LOG_LEVEL",
        converter=parse_log_level,
        validator=validate_log_level,
        description="Default logging level",
    )
    module_levels: dict[str, LogLevelStr] = field(
        factory=default_module_levels,
        env_var="PROVIDE_LOG_MODULE_LEVELS",
        converter=parse_module_levels,
        description="Per-module log levels (format: module1:LEVEL,module2:LEVEL)",
    )
    console_formatter: ConsoleFormatterStr = field(
        default=DEFAULT_CONSOLE_FORMATTER,
        env_var="PROVIDE_LOG_CONSOLE_FORMATTER",
        converter=parse_console_formatter,
        description="Console output formatter (key_value or json)",
    )
    logger_name_emoji_prefix_enabled: bool = field(
        default=DEFAULT_LOGGER_NAME_EMOJI_ENABLED,
        env_var="PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED",
        converter=parse_bool_extended,
        description="Enable emoji prefixes based on logger names",
    )
    das_emoji_prefix_enabled: bool = field(
        default=DEFAULT_DAS_EMOJI_ENABLED,
        env_var="PROVIDE_LOG_DAS_EMOJI_ENABLED",
        converter=parse_bool_extended,
        description="Enable Domain-Action-Status emoji prefixes",
    )
    omit_timestamp: bool = field(
        default=DEFAULT_OMIT_TIMESTAMP,
        env_var="PROVIDE_LOG_OMIT_TIMESTAMP",
        converter=parse_bool_extended,
        description="Omit timestamps from console output",
    )
    # File logging configuration
    log_file: Path | None = field(
        default=None,
        env_var="PROVIDE_LOG_FILE",
        converter=path_converter,
        description="Path to log file",
    )
    foundation_setup_log_level: LogLevelStr = field(
        default=DEFAULT_FOUNDATION_SETUP_LOG_LEVEL,
        env_var="FOUNDATION_LOG_LEVEL",
        converter=parse_log_level,
        validator=validate_log_level,
        description="Log level for Foundation internal setup messages",
    )
    foundation_log_output: str = field(
        default=DEFAULT_FOUNDATION_LOG_OUTPUT,
        env_var="FOUNDATION_LOG_OUTPUT",
        converter=parse_foundation_log_output,
        description="Output destination for Foundation internal messages (stderr, stdout, main)",
    )
    rate_limit_enabled: bool = field(
        default=DEFAULT_RATE_LIMIT_ENABLED,
        env_var="PROVIDE_LOG_RATE_LIMIT_ENABLED",
        converter=parse_bool_extended,
        description="Enable rate limiting for log output",
    )
    rate_limit_global: float | None = field(
        default=None,
        env_var="PROVIDE_LOG_RATE_LIMIT_GLOBAL",
        converter=lambda x: parse_float_with_validation(x, min_val=0.0) if x else None,
        description="Global rate limit (logs per second)",
    )
    rate_limit_global_capacity: float | None = field(
        default=None,
        env_var="PROVIDE_LOG_RATE_LIMIT_GLOBAL_CAPACITY",
        converter=lambda x: parse_float_with_validation(x, min_val=0.0) if x else None,
        description="Global rate limit burst capacity",
    )
    rate_limit_per_logger: dict[str, tuple[float, float]] = field(
        factory=default_rate_limits,
        env_var="PROVIDE_LOG_RATE_LIMIT_PER_LOGGER",
        converter=parse_rate_limits,
        description="Per-logger rate limits (format: logger1:rate:capacity,logger2:rate:capacity)",
    )
    rate_limit_emit_warnings: bool = field(
        default=DEFAULT_RATE_LIMIT_EMIT_WARNINGS,
        env_var="PROVIDE_LOG_RATE_LIMIT_EMIT_WARNINGS",
        converter=parse_bool_extended,
        description="Emit warnings when logs are rate limited",
    )
    rate_limit_summary_interval: float = field(
        default=DEFAULT_RATE_LIMIT_GLOBAL,
        env_var="PROVIDE_LOG_RATE_LIMIT_SUMMARY_INTERVAL",
        converter=lambda x: parse_float_with_validation(x, min_val=0.0) if x else DEFAULT_RATE_LIMIT_GLOBAL,
        validator=validate_positive,
        description="Seconds between rate limit summary reports",
    )
    rate_limit_max_queue_size: int = field(
        default=DEFAULT_RATE_LIMIT_GLOBAL_CAPACITY,
        env_var="PROVIDE_LOG_RATE_LIMIT_MAX_QUEUE_SIZE",
        converter=int,
        validator=validate_positive,
        description="Maximum number of logs to queue when rate limited",
    )
    rate_limit_max_memory_mb: float | None = field(
        default=None,
        env_var="PROVIDE_LOG_RATE_LIMIT_MAX_MEMORY_MB",
        converter=lambda x: parse_float_with_validation(x, min_val=0.0) if x else None,
        description="Maximum memory (MB) for queued logs",
    )
    rate_limit_overflow_policy: str = field(
        default=DEFAULT_RATE_LIMIT_OVERFLOW_POLICY,
        env_var="PROVIDE_LOG_RATE_LIMIT_OVERFLOW_POLICY",
        validator=validate_overflow_policy,
        description="Policy when queue is full: drop_oldest, drop_newest, or block",
    )
    # Sanitization configuration
    sanitization_enabled: bool = field(
        default=DEFAULT_SANITIZATION_ENABLED,
        env_var="PROVIDE_LOG_SANITIZATION_ENABLED",
        converter=parse_bool_extended,
        description="Enable automatic sanitization of sensitive data in logs",
    )
    sanitization_mask_patterns: bool = field(
        default=DEFAULT_SANITIZATION_MASK_PATTERNS,
        env_var="PROVIDE_LOG_SANITIZATION_MASK_PATTERNS",
        converter=parse_bool_extended,
        description="Enable pattern-based secret masking (API keys, tokens, passwords)",
    )
    sanitization_sanitize_dicts: bool = field(
        default=DEFAULT_SANITIZATION_SANITIZE_DICTS,
        env_var="PROVIDE_LOG_SANITIZATION_SANITIZE_DICTS",
        converter=parse_bool_extended,
        description="Enable sanitization of dictionary values (headers, config, etc.)",
    )


# 🧱🏗️🔚
