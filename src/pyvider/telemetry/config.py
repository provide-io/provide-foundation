#
# config.py
#
"""
Pyvider Telemetry Configuration Module.

This module is central to configuring the `pyvider-telemetry` library. It defines
the data models for all telemetry and logging settings, primarily through the
`TelemetryConfig` and `LoggingConfig` classes (built with `attrs`).

Core responsibilities and features include:

- **Configuration Data Models**:
    - `TelemetryConfig`: The main configuration class, encompassing overall
      settings like `service_name` and global telemetry disablement.
    - `LoggingConfig`: A nested configuration class within `TelemetryConfig`,
      specifically for controlling logging behavior. This includes:
        - `default_level`: The default logging severity (e.g., "DEBUG", "INFO").
        - `module_levels`: A dictionary for overriding log levels for specific
          modules (e.g., `{"my_module.utils": "WARNING"}`).
        - `console_formatter`: Specifies the output format for console logging,
          typically "key_value" or "json".
        - `logger_name_emoji_prefix_enabled`: Toggles the emoji prefix based on
          the logger's name.
        - `das_emoji_prefix_enabled`: Toggles the Domain-Action-Status (DAS)
          emoji prefix for semantic logging.
        - `omit_timestamp`: Controls whether timestamps are included in log output.

- **Environment Variable Parsing**:
    - The `TelemetryConfig.from_env()` class method automatically populates the
      configuration from environment variables (e.g., `PYVIDER_LOG_LEVEL`,
      `PYVIDER_LOG_CONSOLE_FORMATTER`, `OTEL_SERVICE_NAME`).
    - It provides sensible defaults for all settings, allowing for
      zero-configuration usage if environment variables are not set.

- **Default Settings and Validation**:
    - Establishes default values for all configuration parameters.
    - Includes logic to handle and warn about invalid environment variable values,
      falling back to defaults to ensure robust operation.

- **Processor Chain Definition**:
    - Contains helper functions that assemble the chain of `structlog` processors
      (e.g., for timestamping, service name injection, emoji handling, level filtering,
      and final formatting) based on the active `TelemetryConfig`.

The configuration object produced by this module, typically via `TelemetryConfig.from_env()`,
is consumed by `pyvider.telemetry.core.setup_telemetry()` to initialize and apply
the desired logging behavior across the application.
"""

import json
import logging as stdlib_logging
import os
import sys
from typing import TYPE_CHECKING, Any, TextIO, cast  # TextIO will be kept

from attrs import define, field
import structlog

from pyvider.telemetry.logger.custom_processors import (
    StructlogProcessor,  # This is an alias for a callable, effectively AnyCallable
    add_das_emoji_prefix,
    add_log_level_custom,
    add_logger_name_emoji_prefix,
    filter_by_level_custom,
)
from pyvider.telemetry.types import (
    _VALID_FORMATTER_TUPLE,  # Now comes from types.py
    _VALID_LOG_LEVEL_TUPLE,  # Now comes from types.py
    TRACE_LEVEL_NUM,  # Now comes from types.py
    ConsoleFormatterStr,
    LogLevelStr,
)

if TYPE_CHECKING:
    pass

# Level mapping using types imported or defined locally
_LEVEL_TO_NUMERIC: dict[LogLevelStr, int] = { # LogLevelStr is now imported
    "CRITICAL": stdlib_logging.CRITICAL,
    "ERROR": stdlib_logging.ERROR,
    "WARNING": stdlib_logging.WARNING,
    "INFO": stdlib_logging.INFO,
    "DEBUG": stdlib_logging.DEBUG,
    "TRACE": TRACE_LEVEL_NUM, # TRACE_LEVEL_NUM is now imported
    "NOTSET": stdlib_logging.NOTSET,
}

# Default environment configuration for zero-config usage (emoji settings handled conditionally)
DEFAULT_ENV_CONFIG: dict[str, str] = {
    "PYVIDER_LOG_LEVEL": "DEBUG", # Default log level
    "PYVIDER_LOG_CONSOLE_FORMATTER": "key_value", # Default formatter
    "PYVIDER_LOG_OMIT_TIMESTAMP": "false", # By default, include timestamps
    "PYVIDER_TELEMETRY_DISABLED": "false", # Telemetry enabled by default
    "PYVIDER_LOG_MODULE_LEVELS": "", # No module-specific levels by default
    # Note: Emoji settings are set conditionally in _apply_default_env_config()
}

# Configuration warnings logger
config_warnings_logger = stdlib_logging.getLogger("pyvider.telemetry.config_warnings")
_config_warning_formatter = stdlib_logging.Formatter(
    "[Pyvider Config Warning] %(levelname)s (%(name)s): %(message)s" # Standard format for config warnings
)

# Store original stdio streams at module load time
_ORIGINAL_SYS_STDOUT = sys.stdout # Keep for reference if needed elsewhere, but not for stream closing here.
_ORIGINAL_SYS_STDERR = sys.stderr # Keep for reference if needed elsewhere.

def _ensure_config_logger_handler(logger: stdlib_logging.Logger) -> None:
    """
    Ensures the config warnings logger has one specifically configured StreamHandler
    pointing to the current sys.stderr. Other handlers are removed.
    No streams from removed handlers are closed by this function.

    Args:
        logger: The standard library logger instance to configure.
    """
    # Remove all existing handlers to ensure a clean state.
    # This is simpler and more robust than trying to find and modify a specific handler.
    for handler in list(logger.handlers): # Iterate over a copy of the list
        logger.removeHandler(handler)
        # DO NOT CLOSE handler.stream here, as it might be sys.stderr or another shared stream.

    # Add our specific handler that writes to the current sys.stderr.
    stderr_handler = stdlib_logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(_config_warning_formatter)
    logger.addHandler(stderr_handler)

    # Ensure the logger is enabled for WARNING level and does not propagate to parent loggers.
    logger.setLevel(stdlib_logging.WARNING) # Only show warnings and above for config issues
    logger.propagate = False # Prevent duplicate messages if parent loggers have handlers


@define(frozen=True, slots=True)
class LoggingConfig:
    """
    Configuration specific to logging behavior within Pyvider Telemetry.

    This class defines settings that control how log messages are processed and
    displayed, such as log levels, output formats, and decorative elements
    like emojis. It is typically nested within `TelemetryConfig`.

    Attributes:
        default_level: The default logging level (e.g., "DEBUG", "INFO") applied
            to all loggers unless overridden by `module_levels`.
        module_levels: A dictionary mapping module names (e.g., "my_app.utils")
            to specific `LogLevelStr` values, allowing for fine-grained control
            over log verbosity for different parts of an application.
        console_formatter: Defines the format of log messages written to the
            console. Valid options are "key_value" (human-readable) or "json"
            (structured). See `ConsoleFormatterStr`.
        logger_name_emoji_prefix_enabled: If True, prepends an emoji to log messages
            based on the name of the logger instance.
        das_emoji_prefix_enabled: If True, prepends a Domain-Action-Status (DAS)
            emoji sequence (e.g., "[🔑][➡️][✅]") to log messages that include
            `domain`, `action`, and `status` keys.
        omit_timestamp: If True, timestamps will be removed from the log output.
            Defaults to False (timestamps included).
    """
    default_level: LogLevelStr = field(default="DEBUG")
    module_levels: dict[str, LogLevelStr] = field(factory=dict)
    console_formatter: ConsoleFormatterStr = field(default="key_value")
    logger_name_emoji_prefix_enabled: bool = field(default=True)
    das_emoji_prefix_enabled: bool = field(default=True)
    omit_timestamp: bool = field(default=False)


@define(frozen=True, slots=True)
class TelemetryConfig:
    """
    Main configuration object for the Pyvider Telemetry system.

    This class aggregates all settings related to telemetry, including logging
    behavior (via `LoggingConfig`), service identification, and global
    enablement status. It is typically instantiated using `TelemetryConfig.from_env()`.

    Attributes:
        service_name: An optional string that identifies the service or application
            generating the logs. If provided, it's included in log entries.
            Can be set via `OTEL_SERVICE_NAME` or `PYVIDER_SERVICE_NAME`
            environment variables.
        logging: An instance of `LoggingConfig` containing detailed settings for
            log processing and output.
        globally_disabled: If True, all telemetry processing and output are
            bypassed. This provides a master switch to disable logging.
            Can be set via the `PYVIDER_TELEMETRY_DISABLED` environment variable.
    """
    service_name: str | None = field(default=None)
    logging: LoggingConfig = field(factory=LoggingConfig)
    globally_disabled: bool = field(default=False)

    @classmethod
    def from_env(cls) -> "TelemetryConfig":
        """
        Creates a `TelemetryConfig` instance by parsing relevant environment variables.

        This method acts as the primary factory for `TelemetryConfig`. It reads
        predefined environment variables (e.g., `PYVIDER_LOG_LEVEL`,
        `PYVIDER_LOG_CONSOLE_FORMATTER`, `OTEL_SERVICE_NAME`,
        `PYVIDER_LOG_MODULE_LEVELS`) to populate the configuration settings.
        If variables are not set, it applies sensible defaults, enabling
        zero-configuration usage. Warnings are issued for invalid values,
        and defaults are used in such cases.

        Key Environment Variables Used:
        - `PYVIDER_LOG_LEVEL`: Sets the default log level.
        - `PYVIDER_LOG_CONSOLE_FORMATTER`: Sets the console output format.
        - `PYVIDER_LOG_OMIT_TIMESTAMP`: Controls timestamp visibility.
        - `PYVIDER_TELEMETRY_DISABLED`: Globally disables telemetry.
        - `PYVIDER_LOG_MODULE_LEVELS`: Comma-separated module-specific levels
          (e.g., "module1:DEBUG,module2.sub:WARNING").
        - `PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED`: Toggles logger name emojis.
        - `PYVIDER_LOG_DAS_EMOJI_ENABLED`: Toggles DAS emojis.
        - `PYVIDER_SERVICE_NAME` or `OTEL_SERVICE_NAME`: Sets the service name.

        Returns:
            A new `TelemetryConfig` instance populated from the environment
            or default values.
        """
        _apply_default_env_config() # Ensure defaults are set if env vars are missing

        # Load service name, preferring OTEL_SERVICE_NAME if available
        service_name_env: str | None = os.getenv(
            "OTEL_SERVICE_NAME", os.getenv("PYVIDER_SERVICE_NAME")
        )

        # Load and validate the default log level
        raw_default_log_level: str = os.getenv("PYVIDER_LOG_LEVEL", "DEBUG").upper()
        default_log_level: LogLevelStr
        if raw_default_log_level in _VALID_LOG_LEVEL_TUPLE:
            default_log_level = cast(LogLevelStr, raw_default_log_level)
        else:
            _ensure_config_logger_handler(config_warnings_logger)
            config_warnings_logger.warning(
                f"⚙️➡️⚠️ Invalid PYVIDER_LOG_LEVEL '{raw_default_log_level}'. Defaulting to DEBUG."
            )
            default_log_level = "DEBUG" # Fallback to a safe default

        # Load and validate the console formatter type
        raw_console_formatter: str = os.getenv(
            "PYVIDER_LOG_CONSOLE_FORMATTER", "key_value"
        ).lower()
        console_formatter: ConsoleFormatterStr
        if raw_console_formatter in _VALID_FORMATTER_TUPLE:
            console_formatter = cast(ConsoleFormatterStr, raw_console_formatter)
        else:
            _ensure_config_logger_handler(config_warnings_logger)
            config_warnings_logger.warning(
                f"⚙️➡️⚠️ Invalid PYVIDER_LOG_CONSOLE_FORMATTER '{raw_console_formatter}'. Defaulting to 'key_value'."
            )
            console_formatter = "key_value" # Fallback to a safe default

        # Load boolean configuration options, with emoji defaults dependent on the formatter
        logger_name_emoji_enabled: bool = _parse_bool_env_with_formatter_default(
            "PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED", console_formatter
        )
        das_emoji_enabled: bool = _parse_bool_env_with_formatter_default(
            "PYVIDER_LOG_DAS_EMOJI_ENABLED", console_formatter
        )
        omit_timestamp: bool = _parse_bool_env("PYVIDER_LOG_OMIT_TIMESTAMP", False)
        globally_disabled: bool = _parse_bool_env("PYVIDER_TELEMETRY_DISABLED", False)

        # Parse module-specific log levels from environment variable
        module_levels_str = os.getenv("PYVIDER_LOG_MODULE_LEVELS", "")
        module_levels = cls._parse_module_levels(module_levels_str)

        # Create the logging configuration object
        log_cfg = LoggingConfig(
            default_level=default_log_level,
            module_levels=module_levels,
            console_formatter=console_formatter,
            logger_name_emoji_prefix_enabled=logger_name_emoji_enabled,
            das_emoji_prefix_enabled=das_emoji_enabled,
            omit_timestamp=omit_timestamp,
        )

        # Create and return the main telemetry configuration object
        return cls(
            service_name=service_name_env,
            logging=log_cfg,
            globally_disabled=globally_disabled,
        )

    @staticmethod
    def _parse_module_levels(levels_str: str) -> dict[str, LogLevelStr]:
        """
        Parses module-specific log level overrides from a comma-separated string.

        The input string should be in the format "module1:LEVEL1,module2:LEVEL2".
        For example, "my_app.utils:WARNING,my_app.services:DEBUG".
        Invalid items or levels within the string will be skipped, and a warning
        will be logged via `config_warnings_logger`.

        Args:
            levels_str: The comma-separated string of module log level overrides,
                typically read from the `PYVIDER_LOG_MODULE_LEVELS` environment
                variable.

        Returns:
            A dictionary mapping module names (as strings) to their configured
            `LogLevelStr` values.
        """
        levels: dict[str, LogLevelStr] = {}
        if not levels_str.strip(): # Return empty if the string is blank
            return levels

        for item in levels_str.split(","):
            item = item.strip()
            if not item: # Skip empty parts resulting from, e.g., "mod1:INFO, ,mod2:DEBUG"
                continue

            parts: list[str] = item.split(":", 1)
            if len(parts) == 2:
                module_name: str = parts[0].strip()
                level_name_raw: str = parts[1].strip().upper()

                if not module_name: # Ensure module name is not empty
                    _ensure_config_logger_handler(config_warnings_logger)
                    config_warnings_logger.warning(
                        f"⚙️➡️⚠️ Empty module name in PYVIDER_LOG_MODULE_LEVELS item '{item}'. Skipping."
                    )
                    continue

                if level_name_raw in _VALID_LOG_LEVEL_TUPLE:
                    levels[module_name] = cast(LogLevelStr, level_name_raw)
                else:
                    _ensure_config_logger_handler(config_warnings_logger)
                    config_warnings_logger.warning(
                        f"⚙️➡️⚠️ Invalid log level '{level_name_raw}' for module '{module_name}' "
                        f"in PYVIDER_LOG_MODULE_LEVELS. Skipping."
                    )
            else: # Handle malformed items
                _ensure_config_logger_handler(config_warnings_logger)
                config_warnings_logger.warning(
                    f"⚙️➡️⚠️ Invalid item '{item}' in PYVIDER_LOG_MODULE_LEVELS. "
                    f"Expected 'module:LEVEL' format. Skipping."
                )
        return levels


def _apply_default_env_config() -> None:
    """
    Applies default environment configuration for Pyvider telemetry variables
    that are not already set in the environment.

    This function enables zero-configuration usage by providing sensible defaults
    for essential settings. Note that emoji-related defaults are handled
    dynamically based on the chosen formatter in `TelemetryConfig.from_env()`.
    """
    for key, default_value in DEFAULT_ENV_CONFIG.items():
        if key not in os.environ: # Set default only if not already defined
            os.environ[key] = default_value

    # Note: Emoji defaults (PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED, PYVIDER_LOG_DAS_EMOJI_ENABLED)
    # are intentionally NOT set here. Their defaults depend on the PYVIDER_LOG_CONSOLE_FORMATTER,
    # so they are handled dynamically in TelemetryConfig.from_env() after the formatter is determined.


def _parse_bool_env(env_var: str, default: bool) -> bool:
    """
    Parses a boolean environment variable, returning a default if not set or invalid.
    Recognizes "true" (case-insensitive) as True, anything else as False.

    Args:
        env_var: The name of the environment variable to parse.
        default: The default boolean value to return if the variable is not set.

    Returns:
        The parsed boolean value.
    """
    value = os.getenv(env_var)
    if value is None:
        return default
    return value.lower() == "true"


def _parse_bool_env_with_formatter_default(env_var: str, formatter: ConsoleFormatterStr) -> bool:
    """
    Parses a boolean environment variable, with default behavior depending on the console formatter.
    If the environment variable is explicitly set, its value is used.
    Otherwise, defaults to True for "key_value" formatter and False for "json" formatter.

    Args:
        env_var: The name of the environment variable.
        formatter: The active console formatter ("key_value" or "json").

    Returns:
        The parsed boolean value.
    """
    value = os.getenv(env_var)
    if value is not None:
        # If explicitly set, parse its value
        return value.lower() == "true"
    else:
        # If not set, default based on formatter type
        # JSON format: emojis are typically off by default for structured logging
        # Key-value format: emojis are on by default for human-readable console output
        from typing import cast
        return cast(bool, formatter == "key_value")


# Processor chain building functions
def _config_create_service_name_processor(service_name: str | None) -> StructlogProcessor:
    """
    Factory for a structlog processor that injects the service name into log events.

    Args:
        service_name: The name of the service, or None.

    Returns:
        A structlog processor function.
    """
    def processor(
        _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        if service_name is not None: # Add service_name if it's defined
            event_dict["service_name"] = service_name
        return event_dict
    return cast(StructlogProcessor, processor)


def _config_create_timestamp_processors(omit_timestamp: bool) -> list[StructlogProcessor]:
    """
    Creates a list of structlog processors for handling timestamps.
    Includes a TimeStamper and optionally a processor to remove the timestamp.

    Args:
        omit_timestamp: If True, adds a processor to remove the timestamp.

    Returns:
        A list of structlog processors.
    """
    # Always add the TimeStamper first to ensure 'timestamp' field is available
    processors: list[StructlogProcessor] = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False) # Local time, ISO-like format
    ]
    if omit_timestamp:
        # If configured, add a processor to remove the 'timestamp' field
        def pop_timestamp_processor(
            _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
        ) -> structlog.types.EventDict:
            event_dict.pop("timestamp", None) # Remove timestamp if present
            return event_dict
        processors.append(cast(StructlogProcessor, pop_timestamp_processor))
    return processors


def _config_create_emoji_processors(logging_config: LoggingConfig) -> list[StructlogProcessor]:
    """
    Creates a list of structlog processors for adding emoji prefixes based on configuration.

    Args:
        logging_config: The LoggingConfig instance containing emoji settings.

    Returns:
        A list of structlog processors for emojis.
    """
    processors: list[StructlogProcessor] = []
    if logging_config.logger_name_emoji_prefix_enabled:
        processors.append(cast(StructlogProcessor, add_logger_name_emoji_prefix))
    if logging_config.das_emoji_prefix_enabled:
        processors.append(cast(StructlogProcessor, add_das_emoji_prefix))
    return processors


def _build_core_processors_list(config: TelemetryConfig) -> list[StructlogProcessor]:
    """
    Builds the core list of structlog processors (excluding final formatter)
    based on the provided TelemetryConfig.

    Args:
        config: The TelemetryConfig instance.

    Returns:
        A list of core structlog processors.
    """
    log_cfg = config.logging
    processors: list[StructlogProcessor] = [
        structlog.contextvars.merge_contextvars, # Merge context variables into the event
        cast(StructlogProcessor, add_log_level_custom), # Add our custom log level (e.g., TRACE)
        cast(StructlogProcessor, filter_by_level_custom( # Filter messages based on configured levels
            default_level_str=log_cfg.default_level, # LogLevelStr type
            module_levels=log_cfg.module_levels, # dict[str, LogLevelStr] type
            level_to_numeric_map=_LEVEL_TO_NUMERIC # Uses LogLevelStr as keys
        )),
        structlog.processors.StackInfoRenderer(),   # Render stack information for exceptions
        structlog.dev.set_exc_info,               # Add exception info to the event
    ]
    # Add timestamp processors (either adds or adds and then removes timestamp)
    processors.extend(_config_create_timestamp_processors(log_cfg.omit_timestamp))

    # Add service name processor if service_name is configured
    if config.service_name is not None:
        processors.append(_config_create_service_name_processor(config.service_name))

    # Add emoji processors based on configuration
    processors.extend(_config_create_emoji_processors(log_cfg))
    return processors


def _config_create_json_formatter_processors() -> list[StructlogProcessor]:
    """
    Creates structlog processors for JSON output formatting.

    Returns:
        A list of processors for JSON formatting.
    """
    return [
        structlog.processors.format_exc_info, # Format exception info for JSON
        structlog.processors.JSONRenderer(serializer=json.dumps, sort_keys=False) # Render as JSON
    ]


def _config_create_keyvalue_formatter_processors(output_stream: TextIO) -> list[StructlogProcessor]:
    """
    Creates structlog processors for key-value (console) output formatting.

    Args:
        output_stream: The TextIO stream where logs will be written (used to check TTY).

    Returns:
        A list of processors for key-value formatting.
    """
    processors: list[StructlogProcessor] = [] # Initialize with Any for ConsoleRenderer if needed

    # Processor to remove 'logger_name' as it's often redundant in console output
    # if emojis or other logger identifiers are used.
    def pop_logger_name_processor(
        _logger: object, _method_name: str, event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        event_dict.pop("logger_name", None)
        return event_dict
    processors.append(cast(StructlogProcessor, pop_logger_name_processor))

    # Determine if output is a TTY to enable/disable colors
    is_tty = hasattr(output_stream, 'isatty') and output_stream.isatty()
    processors.append(
        structlog.dev.ConsoleRenderer(
            colors=is_tty, # Enable colors only if output is a TTY
            exception_formatter=structlog.dev.plain_traceback, # Use plain traceback for exceptions
        )
    )
    return processors # Return type is list[StructlogProcessor] due to ConsoleRenderer being Any


def _build_formatter_processors_list(
    logging_config: LoggingConfig, output_stream: TextIO
) -> list[StructlogProcessor]:
    """
    Builds the list of final formatter processors based on the LoggingConfig.

    Args:
        logging_config: The LoggingConfig instance.
        output_stream: The TextIO stream for output (used by key-value formatter).

    Returns:
        A list of formatter processors.
    """
    match logging_config.console_formatter:
        case "json":
            return _config_create_json_formatter_processors()
        case "key_value":
            return _config_create_keyvalue_formatter_processors(output_stream)
        case unknown_formatter: # Should not happen due to validation in from_env
            _ensure_config_logger_handler(config_warnings_logger)
            config_warnings_logger.warning(
                f"⚙️➡️⚠️ Unknown PYVIDER_LOG_CONSOLE_FORMATTER '{unknown_formatter}' encountered "
                f"during processor list build. Defaulting to 'key_value' formatter."
            )
            return _config_create_keyvalue_formatter_processors(output_stream)

# 🐍⚙️
