"""
Foundation Telemetry Configuration Module.
Defines data models for telemetry and logging settings.
"""

from pathlib import Path
from typing import Any

from attrs import define
import asyncio

from provide.foundation.config import BaseConfig, field
from provide.foundation.config.manager import register_config
from provide.foundation.config.sync import SyncConfigManager
from provide.foundation.logger.emoji.types import (
    CustomDasEmojiSet,
    EmojiSetConfig,
)
from provide.foundation.types import (
    ConsoleFormatterStr,
    LogLevelStr,
)


@define(slots=True, repr=False)
class LoggingConfig(BaseConfig):
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


@define(slots=True, repr=False)
class TelemetryConfig(BaseConfig):
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
        """Creates a TelemetryConfig instance from environment variables using ConfigManager."""
        # Use sync wrapper for backward compatibility
        manager = SyncConfigManager()
        
        # Register the config classes if not already registered
        manager.register("logging", LoggingConfig)
        manager.register("telemetry", cls)
        
        # Load from environment
        telemetry_config = manager.load_from_env("telemetry", cls)
        logging_config = manager.load_from_env("logging", LoggingConfig)
        
        # Combine the configs
        telemetry_config.logging = logging_config
        
        return telemetry_config


# Register configs globally on module import
def _register_configs():
    """Register telemetry configs with global ConfigManager."""
    try:
        asyncio.run(register_config(
            name="logging",
            defaults={
                "default_level": "DEBUG",
                "console_formatter": "key_value",
                "logger_name_emoji_prefix_enabled": True,
                "das_emoji_prefix_enabled": True,
                "omit_timestamp": False,
            }
        ))
        asyncio.run(register_config(
            name="telemetry",
            defaults={
                "globally_disabled": False,
            }
        ))
    except RuntimeError:
        # If we're already in an async context, use sync version
        manager = SyncConfigManager()
        manager.register("logging", LoggingConfig)
        manager.register("telemetry", TelemetryConfig)


_register_configs()