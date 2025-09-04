"""
Foundation Telemetry Configuration Module.
Defines data models for telemetry and logging settings.
"""

import json
import os
from pathlib import Path

from attrs import define

from provide.foundation.config import BaseConfig, field
from provide.foundation.config.types import ConfigSource
from provide.foundation.logger.emoji.types import (
    CustomDasEmojiSet,
    EmojiSetConfig,
)
from provide.foundation.types import (
    ConsoleFormatterStr,
    LogLevelStr,
    _VALID_LOG_LEVEL_TUPLE,
    _VALID_FORMATTER_TUPLE,
)


@define(slots=True, repr=False, frozen=True)
class LoggingConfig:
    """Configuration specific to logging behavior within Foundation Telemetry."""

    default_level: LogLevelStr = field(
        default="DEBUG",
        env_var="PROVIDE_LOG_LEVEL",
        description="Default logging level"
    )
    module_levels: dict[str, LogLevelStr] = field(
        factory=lambda: {},
        env_var="PROVIDE_LOG_MODULE_LEVELS",
        description="Per-module log levels (format: module1:LEVEL,module2:LEVEL)"
    )
    console_formatter: ConsoleFormatterStr = field(
        default="key_value",
        env_var="PROVIDE_LOG_CONSOLE_FORMATTER",
        description="Console output formatter (key_value or json)"
    )
    logger_name_emoji_prefix_enabled: bool = field(
        default=True,
        env_var="PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED",
        description="Enable emoji prefixes based on logger names"
    )
    das_emoji_prefix_enabled: bool = field(
        default=True,
        env_var="PROVIDE_LOG_DAS_EMOJI_ENABLED",
        description="Enable Domain-Action-Status emoji prefixes"
    )
    omit_timestamp: bool = field(
        default=False,
        env_var="PROVIDE_LOG_OMIT_TIMESTAMP",
        description="Omit timestamps from console output"
    )
    enabled_emoji_sets: list[str] = field(
        factory=lambda: [],
        env_var="PROVIDE_LOG_ENABLED_EMOJI_SETS",
        description="Comma-separated list of emoji sets to enable"
    )
    custom_emoji_sets: list[EmojiSetConfig] = field(
        factory=lambda: [],
        env_var="PROVIDE_LOG_CUSTOM_EMOJI_SETS",
        description="JSON array of custom emoji set configurations"
    )
    user_defined_emoji_sets: list[CustomDasEmojiSet] = field(
        factory=lambda: [],
        env_var="PROVIDE_LOG_USER_DEFINED_EMOJI_SETS",
        description="JSON array of user-defined emoji sets"
    )
    log_file: Path | None = field(
        default=None,
        env_var="PROVIDE_LOG_FILE",
        description="Path to log file"
    )

    @classmethod
    def from_env(cls) -> "LoggingConfig":
        """Load LoggingConfig from environment variables."""
        config_dict = {}
        
        # Parse standard fields
        if level := os.getenv("PROVIDE_LOG_LEVEL"):
            level = level.upper()
            if level in _VALID_LOG_LEVEL_TUPLE:
                config_dict["default_level"] = level
        
        if formatter := os.getenv("PROVIDE_LOG_CONSOLE_FORMATTER"):
            formatter = formatter.lower()
            if formatter in _VALID_FORMATTER_TUPLE:
                config_dict["console_formatter"] = formatter
        
        if omit_ts := os.getenv("PROVIDE_LOG_OMIT_TIMESTAMP"):
            config_dict["omit_timestamp"] = omit_ts.lower() == "true"
        
        if logger_emoji := os.getenv("PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED"):
            config_dict["logger_name_emoji_prefix_enabled"] = logger_emoji.lower() == "true"
        
        if das_emoji := os.getenv("PROVIDE_LOG_DAS_EMOJI_ENABLED"):
            config_dict["das_emoji_prefix_enabled"] = das_emoji.lower() == "true"
        
        if log_file := os.getenv("PROVIDE_LOG_FILE"):
            config_dict["log_file"] = Path(log_file)
        
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
            if levels_dict:
                config_dict["module_levels"] = levels_dict
        
        if emoji_sets := os.getenv("PROVIDE_LOG_ENABLED_EMOJI_SETS"):
            config_dict["enabled_emoji_sets"] = [s.strip() for s in emoji_sets.split(",") if s.strip()]
        
        if custom_sets := os.getenv("PROVIDE_LOG_CUSTOM_EMOJI_SETS"):
            try:
                parsed = json.loads(custom_sets)
                if isinstance(parsed, list):
                    config_dict["custom_emoji_sets"] = [
                        EmojiSetConfig(**item) if isinstance(item, dict) else item
                        for item in parsed
                    ]
            except (json.JSONDecodeError, TypeError):
                pass  # Invalid JSON, skip
        
        if user_sets := os.getenv("PROVIDE_LOG_USER_DEFINED_EMOJI_SETS"):
            try:
                parsed = json.loads(user_sets)
                if isinstance(parsed, list):
                    config_dict["user_defined_emoji_sets"] = [
                        CustomDasEmojiSet(**item) if isinstance(item, dict) else item
                        for item in parsed
                    ]
            except (json.JSONDecodeError, TypeError):
                pass  # Invalid JSON, skip
        
        return cls.from_dict(config_dict, source=ConfigSource.ENV)


@define(slots=True, repr=False, frozen=True)
class TelemetryConfig:
    """Main configuration object for the Foundation Telemetry system."""

    service_name: str | None = field(
        default=None,
        env_var="PROVIDE_SERVICE_NAME",
        description="Service name for telemetry"
    )
    logging: LoggingConfig = field(
        factory=LoggingConfig,
        description="Logging configuration"
    )
    globally_disabled: bool = field(
        default=False,
        env_var="PROVIDE_TELEMETRY_DISABLED",
        description="Globally disable telemetry"
    )

    @classmethod
    def from_env(cls) -> "TelemetryConfig":
        """Creates a TelemetryConfig instance from environment variables."""
        config_dict = {}
        
        # Check OTEL_SERVICE_NAME first, then PROVIDE_SERVICE_NAME
        service_name = os.getenv("OTEL_SERVICE_NAME") or os.getenv("PROVIDE_SERVICE_NAME")
        if service_name:
            config_dict["service_name"] = service_name
        
        if disabled := os.getenv("PROVIDE_TELEMETRY_DISABLED"):
            config_dict["globally_disabled"] = disabled.lower() == "true"
        
        # Load logging config from env
        config_dict["logging"] = LoggingConfig.from_env()
        
        return cls.from_dict(config_dict, source=ConfigSource.ENV)