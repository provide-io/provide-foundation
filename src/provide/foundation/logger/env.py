#
# env.py
#
"""
Environment variable parsing for Foundation Telemetry.
"""

import json
import logging as stdlib_logging
import os
import sys
from typing import cast

from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
from provide.foundation.types import (
    _VALID_FORMATTER_TUPLE,
    _VALID_LOG_LEVEL_TUPLE,
    ConsoleFormatterStr,
    CustomDasEmojiSet,
    LogLevelStr,
    SemanticLayer,
    SemanticFieldDefinition,
)

config_warnings_logger = stdlib_logging.getLogger("provide.foundation.config_warnings")
_config_warning_formatter = stdlib_logging.Formatter(
    "[Foundation Config Warning] %(levelname)s (%(name)s): %(message)s"
)

DEFAULT_ENV_CONFIG: dict[str, str] = {
    "FOUNDATION_LOG_LEVEL": "DEBUG",
    "FOUNDATION_LOG_CONSOLE_FORMATTER": "key_value",
    "FOUNDATION_LOG_OMIT_TIMESTAMP": "false",
    "FOUNDATION_TELEMETRY_DISABLED": "false",
    "FOUNDATION_LOG_MODULE_LEVELS": "",
    "FOUNDATION_LOG_ENABLED_SEMANTIC_LAYERS": "",
}


def _ensure_config_logger_handler(logger: stdlib_logging.Logger) -> None:
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
    stderr_handler = stdlib_logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(_config_warning_formatter)
    logger.addHandler(stderr_handler)
    logger.setLevel(stdlib_logging.WARNING)
    logger.propagate = False


def from_env() -> "TelemetryConfig":
    """Creates a `TelemetryConfig` instance by parsing relevant environment variables."""
    _apply_default_env_config()

    service_name_env: str | None = os.getenv(
        "OTEL_SERVICE_NAME", os.getenv("FOUNDATION_SERVICE_NAME")
    )

    raw_default_log_level: str = os.getenv("FOUNDATION_LOG_LEVEL", "DEBUG").upper()
    default_log_level: LogLevelStr
    if raw_default_log_level in _VALID_LOG_LEVEL_TUPLE:
        default_log_level = cast(LogLevelStr, raw_default_log_level)
    else:
        _ensure_config_logger_handler(config_warnings_logger)
        config_warnings_logger.warning(
            f"⚙️➡️⚠️ Invalid FOUNDATION_LOG_LEVEL '{raw_default_log_level}'. Defaulting to DEBUG."
        )
        default_log_level = "DEBUG"

    raw_console_formatter: str = os.getenv(
        "FOUNDATION_LOG_CONSOLE_FORMATTER", "key_value"
    ).lower()
    console_formatter: ConsoleFormatterStr
    if raw_console_formatter in _VALID_FORMATTER_TUPLE:
        console_formatter = cast(ConsoleFormatterStr, raw_console_formatter)
    else:
        _ensure_config_logger_handler(config_warnings_logger)
        config_warnings_logger.warning(
            f"⚙️➡️⚠️ Invalid FOUNDATION_LOG_CONSOLE_FORMATTER '{raw_console_formatter}'. Defaulting to 'key_value'."
        )
        console_formatter = "key_value"

    logger_name_emoji_enabled: bool = _parse_bool_env_with_formatter_default(
        "FOUNDATION_LOG_LOGGER_NAME_EMOJI_ENABLED", console_formatter
    )
    das_emoji_enabled: bool = _parse_bool_env_with_formatter_default(
        "FOUNDATION_LOG_DAS_EMOJI_ENABLED", console_formatter
    )
    omit_timestamp: bool = _parse_bool_env("FOUNDATION_LOG_OMIT_TIMESTAMP", False)
    globally_disabled: bool = _parse_bool_env("FOUNDATION_TELEMETRY_DISABLED", False)

    module_levels = _parse_module_levels(os.getenv("FOUNDATION_LOG_MODULE_LEVELS", ""))
    enabled_semantic_layers = [
        layer.strip()
        for layer in os.getenv("FOUNDATION_LOG_ENABLED_SEMANTIC_LAYERS", "").split(",")
        if layer.strip()
    ]

    custom_semantic_layers = _parse_custom_layers_from_env()
    user_defined_emoji_sets = _parse_user_emoji_sets_from_env()

    log_cfg = LoggingConfig(
        default_level=default_log_level,
        module_levels=module_levels,
        console_formatter=console_formatter,
        logger_name_emoji_prefix_enabled=logger_name_emoji_enabled,
        das_emoji_prefix_enabled=das_emoji_enabled,
        omit_timestamp=omit_timestamp,
        enabled_semantic_layers=enabled_semantic_layers,
        custom_semantic_layers=custom_semantic_layers,
        user_defined_emoji_sets=user_defined_emoji_sets,
    )

    return TelemetryConfig(
        service_name=service_name_env,
        logging=log_cfg,
        globally_disabled=globally_disabled,
    )


def _parse_custom_layers_from_env() -> list[SemanticLayer]:
    custom_layers_json = os.getenv("FOUNDATION_LOG_CUSTOM_SEMANTIC_LAYERS", "[]")
    custom_semantic_layers: list[SemanticLayer] = []
    try:
        parsed_custom_layers = json.loads(custom_layers_json)
        if not isinstance(parsed_custom_layers, list):
            return []
        for layer_data in parsed_custom_layers:
            try:
                if not isinstance(layer_data, dict):
                    continue
                emoji_sets_data = layer_data.get("emoji_sets", [])
                field_defs_data = layer_data.get("field_definitions", [])
                custom_emoji_sets_for_layer = [
                    CustomDasEmojiSet(**es_data)
                    for es_data in emoji_sets_data
                    if isinstance(es_data, dict)
                ]
                custom_field_defs_for_layer = [
                    SemanticFieldDefinition(**fd_data)
                    for fd_data in field_defs_data
                    if isinstance(fd_data, dict)
                ]
                custom_semantic_layers.append(
                    SemanticLayer(
                        name=layer_data.get("name", "unnamed_custom_layer"),
                        description=layer_data.get("description"),
                        emoji_sets=custom_emoji_sets_for_layer,
                        field_definitions=custom_field_defs_for_layer,
                        priority=layer_data.get("priority", 0),
                    )
                )
            except (TypeError, ValueError) as e:
                _ensure_config_logger_handler(config_warnings_logger)
                config_warnings_logger.warning(
                    f"⚙️➡️⚠️ Error parsing data for a custom layer: {e}. Skipping item."
                )
    except json.JSONDecodeError:
        _ensure_config_logger_handler(config_warnings_logger)
        config_warnings_logger.warning(
            "⚙️➡️⚠️ Invalid JSON in FOUNDATION_LOG_CUSTOM_SEMANTIC_LAYERS. Using empty list."
        )
    return custom_semantic_layers


def _parse_user_emoji_sets_from_env() -> list[CustomDasEmojiSet]:
    user_sets_json = os.getenv("FOUNDATION_LOG_USER_DEFINED_EMOJI_SETS", "[]")
    user_defined_emoji_sets: list[CustomDasEmojiSet] = []
    try:
        parsed_user_sets = json.loads(user_sets_json)
        if not isinstance(parsed_user_sets, list):
            return []
        for set_data in parsed_user_sets:
            try:
                if isinstance(set_data, dict):
                    user_defined_emoji_sets.append(CustomDasEmojiSet(**set_data))
            except (TypeError, ValueError) as e:
                _ensure_config_logger_handler(config_warnings_logger)
                config_warnings_logger.warning(
                    f"⚙️➡️⚠️ Error parsing data for an emoji set: {e}. Skipping item."
                )
    except json.JSONDecodeError:
        _ensure_config_logger_handler(config_warnings_logger)
        config_warnings_logger.warning(
            "⚙️➡️⚠️ Invalid JSON in FOUNDATION_LOG_USER_DEFINED_EMOJI_SETS. Using empty list."
        )
    return user_defined_emoji_sets


def _parse_module_levels(levels_str: str) -> dict[str, LogLevelStr]:
    levels: dict[str, LogLevelStr] = {}
    if not levels_str.strip():
        return levels
    for item in levels_str.split(","):
        item = item.strip()
        if not item:
            continue
        parts = item.split(":", 1)
        if len(parts) == 2 and parts[0].strip():
            module_name, level_name_raw = parts[0].strip(), parts[1].strip().upper()
            if level_name_raw in _VALID_LOG_LEVEL_TUPLE:
                levels[module_name] = cast(LogLevelStr, level_name_raw)
            else:
                _ensure_config_logger_handler(config_warnings_logger)
                config_warnings_logger.warning(
                    f"⚙️➡️⚠️ Invalid log level '{level_name_raw}' for module '{module_name}'. Skipping."
                )
        else:
            _ensure_config_logger_handler(config_warnings_logger)
            config_warnings_logger.warning(
                f"⚙️➡️⚠️ Invalid item '{item}' in FOUNDATION_LOG_MODULE_LEVELS. Skipping."
            )
    return levels


def _apply_default_env_config() -> None:
    for key, default_value in DEFAULT_ENV_CONFIG.items():
        os.environ.setdefault(key, default_value)


def _parse_bool_env(env_var: str, default: bool) -> bool:
    value = os.getenv(env_var)
    return value.lower() == "true" if value is not None else default


def _parse_bool_env_with_formatter_default(
    env_var: str, formatter: ConsoleFormatterStr
) -> bool:
    value = os.getenv(env_var)
    return value.lower() == "true" if value is not None else (formatter == "key_value")
