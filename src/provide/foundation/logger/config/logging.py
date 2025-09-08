#
# logging.py
#
"""
LoggingConfig class for Foundation logger configuration.
"""

import json
import os
from pathlib import Path

from attrs import define

from provide.foundation.config import BaseConfig, field
from provide.foundation.config.types import ConfigSource
from provide.foundation.logger.config.base import get_config_logger
from provide.foundation.eventsets.types import EventMapping, EventSet
from provide.foundation.types import (
    _VALID_FORMATTER_TUPLE,
    _VALID_LOG_LEVEL_TUPLE,
    ConsoleFormatterStr,
    LogLevelStr,
)


@define(slots=True, repr=False)
class LoggingConfig(BaseConfig):
    """Configuration specific to logging behavior within Foundation Telemetry."""

    default_level: LogLevelStr = field(
        default="WARNING",
        env_var="PROVIDE_LOG_LEVEL",
        description="Default logging level",
    )
    module_levels: dict[str, LogLevelStr] = field(
        factory=lambda: {},
        env_var="PROVIDE_LOG_MODULE_LEVELS",
        description="Per-module log levels (format: module1:LEVEL,module2:LEVEL)",
    )
    console_formatter: ConsoleFormatterStr = field(
        default="key_value",
        env_var="PROVIDE_LOG_CONSOLE_FORMATTER",
        description="Console output formatter (key_value or json)",
    )
    logger_name_emoji_prefix_enabled: bool = field(
        default=True,
        env_var="PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED",
        description="Enable emoji prefixes based on logger names",
    )
    das_emoji_prefix_enabled: bool = field(
        default=True,
        env_var="PROVIDE_LOG_DAS_EMOJI_ENABLED",
        description="Enable Domain-Action-Status emoji prefixes",
    )
    omit_timestamp: bool = field(
        default=False,
        env_var="PROVIDE_LOG_OMIT_TIMESTAMP",
        description="Omit timestamps from console output",
    )
    enabled_emoji_sets: list[str] = field(
        factory=lambda: [],
        env_var="PROVIDE_LOG_ENABLED_EMOJI_SETS",
        description="Comma-separated list of emoji sets to enable",
    )
    custom_emoji_sets: list[EventSet] = field(
        factory=lambda: [],
        env_var="PROVIDE_LOG_CUSTOM_EMOJI_SETS",
        description="JSON array of custom emoji set configurations",
    )
    user_defined_emoji_sets: list[EventMapping] = field(
        factory=lambda: [],
        env_var="PROVIDE_LOG_USER_DEFINED_EMOJI_SETS",
        description="JSON array of user-defined emoji sets",
    )
    log_file: Path | None = field(
        default=None, env_var="PROVIDE_LOG_FILE", description="Path to log file"
    )
    foundation_setup_log_level: LogLevelStr = field(
        default="INFO",
        env_var="FOUNDATION_LOG_LEVEL",
        description="Log level for Foundation internal setup messages",
    )
    foundation_log_output: str = field(
        default="stderr",
        env_var="FOUNDATION_LOG_OUTPUT",
        description="Output destination for Foundation internal messages (stderr, stdout, main)",
    )
    show_emoji_matrix: bool = field(
        default=False,
        env_var="PROVIDE_SHOW_EMOJI_MATRIX",
        description="Whether to display emoji matrix on startup",
    )
    rate_limit_enabled: bool = field(
        default=False,
        env_var="PROVIDE_LOG_RATE_LIMIT_ENABLED",
        description="Enable rate limiting for log output",
    )
    rate_limit_global: float | None = field(
        default=None,
        env_var="PROVIDE_LOG_RATE_LIMIT_GLOBAL",
        description="Global rate limit (logs per second)",
    )
    rate_limit_global_capacity: float | None = field(
        default=None,
        env_var="PROVIDE_LOG_RATE_LIMIT_GLOBAL_CAPACITY",
        description="Global rate limit burst capacity",
    )
    rate_limit_per_logger: dict[str, tuple[float, float]] = field(
        factory=lambda: {},
        env_var="PROVIDE_LOG_RATE_LIMIT_PER_LOGGER",
        description="Per-logger rate limits (format: logger1:rate:capacity,logger2:rate:capacity)",
    )
    rate_limit_emit_warnings: bool = field(
        default=True,
        env_var="PROVIDE_LOG_RATE_LIMIT_EMIT_WARNINGS",
        description="Emit warnings when logs are rate limited",
    )
    rate_limit_summary_interval: float = field(
        default=5.0,
        env_var="PROVIDE_LOG_RATE_LIMIT_SUMMARY_INTERVAL",
        description="Seconds between rate limit summary reports",
    )
    rate_limit_max_queue_size: int = field(
        default=1000,
        env_var="PROVIDE_LOG_RATE_LIMIT_MAX_QUEUE_SIZE",
        description="Maximum number of logs to queue when rate limited",
    )
    rate_limit_max_memory_mb: float | None = field(
        default=None,
        env_var="PROVIDE_LOG_RATE_LIMIT_MAX_MEMORY_MB",
        description="Maximum memory (MB) for queued logs",
    )
    rate_limit_overflow_policy: str = field(
        default="drop_oldest",
        env_var="PROVIDE_LOG_RATE_LIMIT_OVERFLOW_POLICY",
        description="Policy when queue is full: drop_oldest, drop_newest, or block",
    )

    @classmethod
    def from_env(cls, strict: bool = True) -> "LoggingConfig":
        """Load LoggingConfig from environment variables."""
        config_dict = {}

        # Parse standard fields
        if level := os.getenv("PROVIDE_LOG_LEVEL"):
            level = level.upper()
            if level in _VALID_LOG_LEVEL_TUPLE:
                config_dict["default_level"] = level
            elif strict:
                get_config_logger().warning(
                    "[Foundation Config Warning] Invalid configuration value, using default",
                    config_key="PROVIDE_LOG_LEVEL",
                    invalid_value=level,
                    valid_options=list(_VALID_LOG_LEVEL_TUPLE),
                    default_value="DEBUG",
                )

        if formatter := os.getenv("PROVIDE_LOG_CONSOLE_FORMATTER"):
            formatter = formatter.lower()
            if formatter in _VALID_FORMATTER_TUPLE:
                config_dict["console_formatter"] = formatter
            elif strict:
                get_config_logger().warning(
                    "[Foundation Config Warning] Invalid configuration value, using default",
                    config_key="PROVIDE_LOG_CONSOLE_FORMATTER",
                    invalid_value=formatter,
                    valid_options=list(_VALID_FORMATTER_TUPLE),
                    default_value="key_value",
                )

        if omit_ts := os.getenv("PROVIDE_LOG_OMIT_TIMESTAMP"):
            config_dict["omit_timestamp"] = omit_ts.lower() == "true"

        if logger_emoji := os.getenv("PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED"):
            config_dict["logger_name_emoji_prefix_enabled"] = (
                logger_emoji.lower() == "true"
            )

        if das_emoji := os.getenv("PROVIDE_LOG_DAS_EMOJI_ENABLED"):
            config_dict["das_emoji_prefix_enabled"] = das_emoji.lower() == "true"

        if log_file := os.getenv("PROVIDE_LOG_FILE"):
            config_dict["log_file"] = Path(log_file)

        if foundation_level := os.getenv("FOUNDATION_LOG_LEVEL"):
            foundation_level = foundation_level.upper()
            if foundation_level in _VALID_LOG_LEVEL_TUPLE:
                config_dict["foundation_setup_log_level"] = foundation_level
            elif strict:
                get_config_logger().warning(
                    "[Foundation Config Warning] Invalid configuration value, using default",
                    config_key="FOUNDATION_LOG_LEVEL",
                    invalid_value=foundation_level,
                    valid_options=list(_VALID_LOG_LEVEL_TUPLE),
                    default_value="INFO",
                )

        if foundation_output := os.getenv("FOUNDATION_LOG_OUTPUT"):
            foundation_output = foundation_output.lower()
            valid_outputs = ("stderr", "stdout", "main")
            if foundation_output in valid_outputs:
                config_dict["foundation_log_output"] = foundation_output
            elif strict:
                get_config_logger().warning(
                    "[Foundation Config Warning] Invalid configuration value, using default",
                    config_key="FOUNDATION_LOG_OUTPUT",
                    invalid_value=foundation_output,
                    valid_options=list(valid_outputs),
                    default_value="stderr",
                )

        if show_matrix := os.getenv("PROVIDE_SHOW_EMOJI_MATRIX"):
            config_dict["show_emoji_matrix"] = show_matrix.strip().lower() in (
                "true",
                "1",
                "yes",
            )

        # Parse rate limiting configuration
        if rate_limit_enabled := os.getenv("PROVIDE_LOG_RATE_LIMIT_ENABLED"):
            config_dict["rate_limit_enabled"] = rate_limit_enabled.lower() == "true"

        if rate_limit_global := os.getenv("PROVIDE_LOG_RATE_LIMIT_GLOBAL"):
            try:
                config_dict["rate_limit_global"] = float(rate_limit_global)
            except ValueError:
                if strict:
                    get_config_logger().warning(
                        "[Foundation Config Warning] Invalid rate limit value",
                        config_key="PROVIDE_LOG_RATE_LIMIT_GLOBAL",
                        invalid_value=rate_limit_global,
                    )

        if rate_limit_capacity := os.getenv("PROVIDE_LOG_RATE_LIMIT_GLOBAL_CAPACITY"):
            try:
                config_dict["rate_limit_global_capacity"] = float(rate_limit_capacity)
            except ValueError:
                if strict:
                    get_config_logger().warning(
                        "[Foundation Config Warning] Invalid rate limit capacity",
                        config_key="PROVIDE_LOG_RATE_LIMIT_GLOBAL_CAPACITY",
                        invalid_value=rate_limit_capacity,
                    )

        if per_logger_limits := os.getenv("PROVIDE_LOG_RATE_LIMIT_PER_LOGGER"):
            limits_dict = {}
            for item in per_logger_limits.split(","):
                parts = item.split(":")
                if len(parts) == 3:
                    logger_name, rate, capacity = parts
                    try:
                        limits_dict[logger_name.strip()] = (
                            float(rate.strip()),
                            float(capacity.strip()),
                        )
                    except ValueError:
                        if strict:
                            get_config_logger().warning(
                                "[Foundation Config Warning] Invalid per-logger rate limit",
                                config_key="PROVIDE_LOG_RATE_LIMIT_PER_LOGGER",
                                invalid_item=item,
                            )
            if limits_dict:
                config_dict["rate_limit_per_logger"] = limits_dict

        if emit_warnings := os.getenv("PROVIDE_LOG_RATE_LIMIT_EMIT_WARNINGS"):
            config_dict["rate_limit_emit_warnings"] = emit_warnings.lower() == "true"

        if summary_interval := os.getenv("PROVIDE_LOG_RATE_LIMIT_SUMMARY_INTERVAL"):
            try:
                config_dict["rate_limit_summary_interval"] = float(summary_interval)
            except ValueError:
                if strict:
                    get_config_logger().warning(
                        "[Foundation Config Warning] Invalid summary interval",
                        config_key="PROVIDE_LOG_RATE_LIMIT_SUMMARY_INTERVAL",
                        invalid_value=summary_interval,
                    )

        if max_queue := os.getenv("PROVIDE_LOG_RATE_LIMIT_MAX_QUEUE_SIZE"):
            try:
                config_dict["rate_limit_max_queue_size"] = int(max_queue)
            except ValueError:
                if strict:
                    get_config_logger().warning(
                        "[Foundation Config Warning] Invalid max queue size",
                        config_key="PROVIDE_LOG_RATE_LIMIT_MAX_QUEUE_SIZE",
                        invalid_value=max_queue,
                    )

        if max_memory := os.getenv("PROVIDE_LOG_RATE_LIMIT_MAX_MEMORY_MB"):
            try:
                config_dict["rate_limit_max_memory_mb"] = float(max_memory)
            except ValueError:
                if strict:
                    get_config_logger().warning(
                        "[Foundation Config Warning] Invalid max memory",
                        config_key="PROVIDE_LOG_RATE_LIMIT_MAX_MEMORY_MB",
                        invalid_value=max_memory,
                    )

        if overflow_policy := os.getenv("PROVIDE_LOG_RATE_LIMIT_OVERFLOW_POLICY"):
            valid_policies = ("drop_oldest", "drop_newest", "block")
            if overflow_policy in valid_policies:
                config_dict["rate_limit_overflow_policy"] = overflow_policy
            elif strict:
                get_config_logger().warning(
                    "[Foundation Config Warning] Invalid overflow policy",
                    config_key="PROVIDE_LOG_RATE_LIMIT_OVERFLOW_POLICY",
                    invalid_value=overflow_policy,
                    valid_options=list(valid_policies),
                )

        # Parse complex fields
        if module_levels := os.getenv("PROVIDE_LOG_MODULE_LEVELS"):
            levels_dict = {}
            for item in module_levels.split(","):
                if ":" in item:
                    module, level = item.split(":", 1)
                    module = module.strip()
                    level = level.strip().upper()
                    if module and level in _VALID_LOG_LEVEL_TUPLE:
                        levels_dict[module] = level
                    elif strict and module and level not in _VALID_LOG_LEVEL_TUPLE:
                        get_config_logger().warning(
                            "[Foundation Config Warning] Invalid module log level, skipping",
                            config_key="PROVIDE_LOG_MODULE_LEVELS",
                            module_name=module,
                            invalid_level=level,
                            valid_options=list(_VALID_LOG_LEVEL_TUPLE),
                        )
            if levels_dict:
                config_dict["module_levels"] = levels_dict

        if emoji_sets := os.getenv("PROVIDE_LOG_ENABLED_EMOJI_SETS"):
            config_dict["enabled_emoji_sets"] = [
                s.strip() for s in emoji_sets.split(",") if s.strip()
            ]

        if custom_sets := os.getenv("PROVIDE_LOG_CUSTOM_EMOJI_SETS"):
            try:
                parsed = json.loads(custom_sets)
                if isinstance(parsed, list):
                    config_dict["custom_emoji_sets"] = [
                        EventSet(**item) if isinstance(item, dict) else item
                        for item in parsed
                    ]
            except json.JSONDecodeError as e:
                if strict:
                    get_config_logger().warning(
                        "[Foundation Config Warning] Invalid JSON in configuration",
                        config_key="PROVIDE_LOG_CUSTOM_EMOJI_SETS",
                        error=str(e),
                        config_value=custom_sets[:100] + "..."
                        if len(custom_sets) > 100
                        else custom_sets,
                    )
            except (TypeError, ValueError) as e:
                if strict:
                    get_config_logger().warning(
                        "[Foundation Config Warning] Error parsing custom emoji set configuration",
                        config_key="PROVIDE_LOG_CUSTOM_EMOJI_SETS",
                        error=str(e),
                        error_type=type(e).__name__,
                    )

        if user_sets := os.getenv("PROVIDE_LOG_USER_DEFINED_EMOJI_SETS"):
            try:
                parsed = json.loads(user_sets)
                if isinstance(parsed, list):
                    config_dict["user_defined_emoji_sets"] = [
                        EventMapping(**item) if isinstance(item, dict) else item
                        for item in parsed
                    ]
            except json.JSONDecodeError as e:
                if strict:
                    get_config_logger().warning(
                        "[Foundation Config Warning] Invalid JSON in configuration",
                        config_key="PROVIDE_LOG_USER_DEFINED_EMOJI_SETS",
                        error=str(e),
                        config_value=user_sets[:100] + "..."
                        if len(user_sets) > 100
                        else user_sets,
                    )
            except (TypeError, ValueError) as e:
                if strict:
                    get_config_logger().warning(
                        "[Foundation Config Warning] Error parsing user emoji set configuration",
                        config_key="PROVIDE_LOG_USER_DEFINED_EMOJI_SETS",
                        error=str(e),
                        error_type=type(e).__name__,
                    )

        return cls.from_dict(config_dict, source=ConfigSource.ENV)
