#
# config.py
#
"""
Foundation Telemetry Configuration Module.
Defines data models for telemetry and logging settings.
"""
from pathlib import Path
from attrs import define, field

from provide.foundation.types import (
    ConsoleFormatterStr,
    LogLevelStr,
)
from provide.foundation.logger.emoji.types import (
    CustomDasEmojiSet,
    EmojiSetConfig,
)


@define(frozen=True, slots=True)
class LoggingConfig:
    """Configuration specific to logging behavior within Foundation Telemetry."""

    default_level: LogLevelStr = field(default="DEBUG")
    module_levels: dict[str, LogLevelStr] = field(factory=lambda: {})
    console_formatter: ConsoleFormatterStr = field(default="key_value")
    logger_name_emoji_prefix_enabled: bool = field(default=True)
    das_emoji_prefix_enabled: bool = field(default=True)
    omit_timestamp: bool = field(default=False)
    enabled_emoji_sets: list[str] = field(factory=lambda: [])
    custom_emoji_sets: list[EmojiSetConfig] = field(factory=lambda: [])
    user_defined_emoji_sets: list[CustomDasEmojiSet] = field(factory=lambda: [])
    log_file: Path | None = field(default=None)


@define(frozen=True, slots=True)
class TelemetryConfig:
    """Main configuration object for the Foundation Telemetry system."""

    service_name: str | None = field(default=None)
    logging: LoggingConfig = field(factory=LoggingConfig)
    globally_disabled: bool = field(default=False)

    @classmethod
    def from_env(cls) -> "TelemetryConfig":
        """Creates a `TelemetryConfig` instance by parsing relevant environment variables."""
        from provide.foundation.logger.env import from_env as _from_env

        return _from_env()
