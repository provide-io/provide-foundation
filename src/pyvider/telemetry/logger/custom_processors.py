#
# custom_processors.py
#
"""
Pyvider Telemetry Custom Structlog Processors.

This module provides a collection of custom `structlog` processors designed to
enhance the logging output and add Pyvider-specific features to the telemetry pipeline.
These processors are integral to how log events are filtered, augmented, and
formatted before final output.

Key Processors and Their Functions:
- `add_log_level_custom`: Ensures each log event has a normalized 'level' field,
  handling custom levels like "TRACE" and method name aliases (e.g., `warn`
  to "warning").
- `filter_by_level_custom` (factory for `_LevelFilter`): Implements hierarchical
  log filtering based on a default log level and module-specific overrides. This
  allows for fine-grained control over log verbosity across different parts of
  an application by potentially dropping events.
- `add_logger_name_emoji_prefix`: Prepends an emoji to the log message based on
  the logger's name. This adds quick visual context to logs and is optimized
  with a cache for frequently used logger names.
- `add_das_emoji_prefix`: Implements semantic logging by prepending a
  Domain-Action-Status (DAS) emoji sequence (e.g., "[🔑][➡️][✅]") based on
  `domain`, `action`, and `status` keys in the event dictionary. This provides
  structured, at-a-glance meaning to log events by transforming these keys
  into visual cues and then removing the original keys.

These processors are typically assembled into a chain by the functions in
`pyvider.telemetry.config` and applied during the `structlog` configuration
in `pyvider.telemetry.core`. They work together to create informative,
semantically rich, and visually parseable log output.
"""
import logging as stdlib_logging
from typing import TYPE_CHECKING, Any, Protocol, cast

import structlog

from pyvider.telemetry.logger.emoji_matrix import (
    PRIMARY_EMOJI,
    SECONDARY_EMOJI,
    TERTIARY_EMOJI,
)

# Updated import for LogLevelStr, and new imports for TRACE constants
from pyvider.telemetry.types import (
    TRACE_LEVEL_NAME,
    TRACE_LEVEL_NUM,
    LogLevelStr,
)

if TYPE_CHECKING:
    # Type checking imports
    pass

# TRACE_LEVEL_NUM and TRACE_LEVEL_NAME are now imported from pyvider.telemetry.types
# The registration of the TRACE level with stdlib_logging is also done in types.py

# Mapping of numeric levels to string names for efficient lookup
_NUMERIC_TO_LEVEL_NAME_CUSTOM: dict[int, str] = {
    stdlib_logging.CRITICAL: "critical",
    stdlib_logging.ERROR: "error",
    stdlib_logging.WARNING: "warning",
    stdlib_logging.INFO: "info",
    stdlib_logging.DEBUG: "debug",
    TRACE_LEVEL_NUM: TRACE_LEVEL_NAME.lower(),
}

class StructlogProcessor(Protocol):
    """
    Defines the expected interface for a `structlog` processor function.

    A processor is a callable that receives the logger instance, the name of
    the logging method that was called, and the current event dictionary.
    It then processes and returns the (potentially modified) event dictionary.
    Processors can also choose to drop an event by raising `structlog.DropEvent`.
    """
    def __call__(
        self,
        logger: Any,  # The logger instance, often unused by processors.
        method_name: str,  # Name of the logging method (e.g., 'info', 'debug').
        event_dict: structlog.types.EventDict  # The event dictionary.
    ) -> structlog.types.EventDict:
        """
        Processes a log event dictionary.

        Args:
            logger: The logger instance (often unused by processors).
            method_name: The name of the logging method called (e.g., 'info', 'error').
            event_dict: The dictionary representing the log event to be processed.

        Returns:
            The (potentially modified) event dictionary.

        Raises:
            structlog.DropEvent: If the processor decides the event should not
                be processed further and thus dropped.
        """
        ...

def add_log_level_custom(
    _logger: Any, method_name: str, event_dict: structlog.types.EventDict
) -> structlog.types.EventDict:
    """
    Adds or normalizes the 'level' field in the log event dictionary.

    This processor ensures a consistent 'level' field for all log events.
    It operates as follows:
    1. If a `_pyvider_level_hint` key exists in `event_dict` (used internally,
       especially for the custom TRACE level), its value is used as the log level
       (converted to lowercase) and the hint is removed.
    2. If `_pyvider_level_hint` is not present and `event_dict` does not already
       contain a 'level' key, the `method_name` (e.g., "info", "error", "debug",
       "warn", "exception") is used to derive the level.
       - "exception" maps to "error".
       - "warn" maps to "warning".
       - "msg" maps to "info" (a common `structlog` method for level-agnostic messages).
       - Other method names are converted to lowercase.
    3. If a 'level' key already exists, it is preserved.

    Args:
        _logger (Any): The logger instance (unused by this processor).
        method_name (str): The name of the logging method that was called
            (e.g., 'info', 'debug').
        event_dict (structlog.types.EventDict): The log event dictionary being processed.

    Returns:
        structlog.types.EventDict: The event dictionary, guaranteed to have a 'level'
            key, with the `_pyvider_level_hint` removed if it was present.
    """
    # Check for custom level hint (used for TRACE level)
    level_hint: str | None = event_dict.pop("_pyvider_level_hint", None)

    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
        # Map method names to standard log levels
        match method_name:
            case "exception":
                event_dict["level"] = "error"
            case "warn":
                event_dict["level"] = "warning"
            case "msg":
                event_dict["level"] = "info"
            case _:
                event_dict["level"] = method_name.lower()

    return event_dict

class _LevelFilter:
    """
    Callable filter for log events based on configured log levels.

    This class implements a hierarchical logging system. It determines the
    effective log level for a given logger (considering both a default level
    and module-specific overrides) and then compares the event's log level
    against this threshold. If the event's level is lower than the threshold,
    `structlog.DropEvent` is raised to suppress the event.

    Module-specific levels override the default level. When matching module names,
    the longest matching module path takes precedence (e.g., a rule for
    "my_app.module" will be chosen over a rule for "my_app").

    Attributes:
        default_numeric_level (int): The numeric representation of the default
            log level.
        module_numeric_levels (dict[str, int]): A dictionary mapping module name
            prefixes to their numeric log level thresholds.
        level_to_numeric_map (dict[LogLevelStr, int]): A dictionary mapping
            log level string names (e.g., "INFO", "DEBUG") to their numeric values.
        sorted_module_paths (list[str]): Module paths from `module_numeric_levels`
            sorted by length in descending order to ensure longest-prefix matching.
    """

    def __init__(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int]
    ) -> None:
        """
        Initializes the level filter with logging configuration.

        Args:
            default_level_str (LogLevelStr): The default log level (e.g., "INFO").
            module_levels (dict[str, LogLevelStr]): A dictionary mapping module
                name strings to `LogLevelStr` values for overrides.
            level_to_numeric_map (dict[LogLevelStr, int]): A dictionary mapping
                `LogLevelStr` values to their corresponding numeric log levels.
        """
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str]
            for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map

        # Sort module paths by length (longest first) for prefix matching
        self.sorted_module_paths: list[str] = sorted(
            self.module_numeric_levels.keys(), key=len, reverse=True
        )

    def __call__(
        self, _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """
        Filters a log event based on its level and the configured thresholds.

        The effective log level for the event's logger (derived from `logger_name`
        in `event_dict`) is determined. If the event's own level is below this
        threshold, `structlog.DropEvent` is raised.

        Args:
            _logger (Any): The logger instance (unused by this filter).
            _method_name (str): The name of the logging method (unused by this filter).
            event_dict (structlog.types.EventDict): The log event dictionary. Must
                contain 'logger_name' (or defaults to "unnamed_filter_target") and
                'level' (or defaults to "info") keys.

        Returns:
            structlog.types.EventDict: The `event_dict` unmodified, if the event
                passes the filter.

        Raises:
            structlog.DropEvent: If the event's log level is below the
                determined threshold for its logger.
        """
        # Extract logger name and event level from the event
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info")).upper()
        event_level_text: LogLevelStr = cast(LogLevelStr, event_level_str_from_dict)

        # Convert event level to numeric for comparison
        event_num_level: int = self.level_to_numeric_map.get(
            event_level_text, self.level_to_numeric_map["INFO"]
        )

        # Determine effective threshold level for this logger
        threshold_num_level: int = self.default_numeric_level

        # Find the most specific module-level override
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break

        # Drop event if it's below the threshold
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent

        return event_dict

def filter_by_level_custom(
    default_level_str: LogLevelStr,
    module_levels: dict[str, LogLevelStr],
    level_to_numeric_map: dict[LogLevelStr, int]
) -> _LevelFilter:
    """
    Factory that creates and returns a configured `_LevelFilter` instance.

    This processor is used to filter log messages based on their level,
    supporting a default level and module-specific overrides.

    Args:
        default_level_str (LogLevelStr): The default log level (e.g., "INFO")
            to be used if no module-specific rule matches.
        module_levels (dict[str, LogLevelStr]): A dictionary mapping module
            name prefixes to `LogLevelStr` values for targeted log verbosity.
        level_to_numeric_map (dict[LogLevelStr, int]): A dictionary that maps
            `LogLevelStr` values to their numeric representations (e.g.,
            `{"INFO": 20, "DEBUG": 10}`).

    Returns:
        _LevelFilter: An initialized `_LevelFilter` object ready to be used
            in a `structlog` processor chain.
    """
    return _LevelFilter(default_level_str, module_levels, level_to_numeric_map)

# Logger name to emoji mapping for visual log parsing
_LOGGER_NAME_EMOJI_PREFIXES: dict[str, str] = {
    'pyvider.telemetry.core.test': '⚙️',
    'pyvider.telemetry.core_setup': '🛠️',
    'pyvider.telemetry.emoji_matrix_display': '💡',
    'pyvider.telemetry': '⚙️',
    'pyvider.telemetry.logger': '📝',
    'pyvider.telemetry.config': '🔩',
    'pyvider.dynamic_call_trace': '👣',
    'pyvider.dynamic_call': '🗣️',
    'pyvider.default': '📦',
    'formatter.test': '🎨',
    'service.alpha': '🇦',
    'service.beta': '🇧',
    'service.beta.child': '👶',
    'service.gamma.trace_enabled': '🇬',
    'service.delta': '🇩',
    'das.test': '🃏',
    'json.exc.test': '💥',
    'service.name.test': '📛',
    'simple': '📄',
    'test.basic': '🧪',
    'unknown': '❓',
    'test': '🧪',
    'default': '🔹',
    'emoji.test': '🎭',  # FIXED: Added mapping for emoji.test
}

# Sort logger name patterns by length (longest first) for prefix matching
_SORTED_LOGGER_NAME_EMOJI_KEYWORDS: list[str] = sorted(
    _LOGGER_NAME_EMOJI_PREFIXES.keys(), key=len, reverse=True
)

# Performance optimization: Cache emoji lookups for frequently used logger names
_EMOJI_LOOKUP_CACHE: dict[str, str] = {}
_EMOJI_CACHE_SIZE_LIMIT: int = 1000  # Prevent unbounded cache growth

def _compute_emoji_for_logger_name(logger_name: str) -> str:
    """
    Computes the appropriate emoji for a given logger name using prefix matching.

    It iterates through `_SORTED_LOGGER_NAME_EMOJI_KEYWORDS` (sorted by length,
    longest first) and returns the emoji for the first matching keyword found
    at the beginning of `logger_name`. If no specific match is found, it returns
    the emoji associated with the "default" key in `_LOGGER_NAME_EMOJI_PREFIXES`,
    or '🔹' if "default" is also missing.

    Args:
        logger_name (str): The name of the logger for which to find an emoji.

    Returns:
        str: The determined emoji string.
    """
    # Find the most specific emoji pattern match
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == 'default':
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]

    # Return default emoji if no match found
    return _LOGGER_NAME_EMOJI_PREFIXES.get('default', '🔹')

def add_logger_name_emoji_prefix(
    _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
) -> structlog.types.EventDict:
    """
    Prepends an emoji to the log 'event' field based on `logger_name`.

    This processor enhances log readability by adding a visual cue (emoji)
    related to the source logger. The selection mechanism uses longest-prefix
    matching against predefined patterns in `_LOGGER_NAME_EMOJI_PREFIXES`.
    To optimize performance for frequently used logger names, results are cached
    in `_EMOJI_LOOKUP_CACHE` up to `_EMOJI_CACHE_SIZE_LIMIT`.

    If the 'event' field in `event_dict` is `None`, the emoji itself becomes
    the event. Otherwise, the emoji is prepended to the existing event string.

    Args:
        _logger (Any): The logger instance (unused).
        _method_name (str): The logging method name (unused).
        event_dict (structlog.types.EventDict): The log event dictionary. Expected
            to contain 'logger_name' (defaults to "default") and 'event'.

    Returns:
        structlog.types.EventDict: The modified `event_dict` with the emoji prefix
            added to the 'event' field.
    """
    logger_name_from_event: str = event_dict.get("logger_name", "default")

    # Check cache first for performance
    if logger_name_from_event in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name_from_event]
    else:
        # Compute emoji and cache the result
        chosen_emoji = _compute_emoji_for_logger_name(logger_name_from_event)

        # Cache management: prevent unbounded growth
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name_from_event] = chosen_emoji
        # If cache is full, we skip caching but still return the computed emoji

    # Prepend emoji to event message
    event_msg: Any = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji

    return event_dict

def add_das_emoji_prefix(
    _logger: Any, _method_name: str, event_dict: structlog.types.EventDict
) -> structlog.types.EventDict:
    """
    Prepends a Domain-Action-Status (DAS) emoji sequence to the 'event' field.

    This processor enhances logs with semantic, visual cues by looking for
    'domain', 'action', and 'status' keys within the `event_dict`. It maps these
    keys to emojis defined in `PRIMARY_EMOJI`, `SECONDARY_EMOJI`, and
    `TERTIARY_EMOJI` respectively. The resulting emoji sequence is formatted as
    `[D_emoji][A_emoji][S_emoji]` and prepended to the log message.

    The original 'domain', 'action', and 'status' keys are removed from the
    `event_dict` after processing to prevent redundancy in the final log output.
    If none of the DAS keys are present, the event message remains unchanged.

    Args:
        _logger (Any): The logger instance (unused).
        _method_name (str): The logging method name (unused).
        event_dict (structlog.types.EventDict): The log event dictionary,
            potentially containing 'domain', 'action', and 'status' keys.

    Returns:
        structlog.types.EventDict: The modified `event_dict` with the DAS emoji
            prefix added to the 'event' field and original DAS keys removed.
    """
    # Extract and remove DAS fields from event dictionary
    domain_val_orig = event_dict.pop("domain", None)
    action_val_orig = event_dict.pop("action", None)
    status_val_orig = event_dict.pop("status", None)

    # Convert to lowercase strings for consistent lookup
    domain_val: str = str(domain_val_orig).lower() if domain_val_orig is not None else ""
    action_val: str = str(action_val_orig).lower() if action_val_orig is not None else ""
    status_val: str = str(status_val_orig).lower() if status_val_orig is not None else ""

    # Only add DAS prefix if at least one field is present
    if domain_val or action_val or status_val:
        # FIXED: Ensure defaults are used for unknown values
        domain_emoji: str = PRIMARY_EMOJI.get(domain_val, PRIMARY_EMOJI.get("default", "❓"))
        action_emoji: str = SECONDARY_EMOJI.get(action_val, SECONDARY_EMOJI.get("default", "⚙️"))
        status_emoji: str = TERTIARY_EMOJI.get(status_val, TERTIARY_EMOJI.get("default", "➡️"))

        # Build DAS prefix in standard format
        das_prefix = f"[{domain_emoji}][{action_emoji}][{status_emoji}]"

        # Prepend DAS prefix to event message
        event_msg: Any = event_dict.get("event")
        if event_msg is not None:
            event_dict["event"] = f"{das_prefix} {event_msg}"
        else:
            event_dict["event"] = das_prefix

    return event_dict

# Performance monitoring functions for cache effectiveness
def get_emoji_cache_stats() -> dict[str, Any]:  # pragma: no cover
    """
    Returns statistics about the logger name emoji lookup cache.

    Provides insights into cache utilization, including current size, limit,
    and utilization percentage. This is primarily intended for debugging and
    performance monitoring of the `add_logger_name_emoji_prefix` processor.

    Returns:
        dict[str, Any]: A dictionary containing:
            - "cache_size": Current number of items in the cache.
            - "cache_limit": Maximum configured size of the cache.
            - "cache_utilization": Cache size as a percentage of the limit.
    """
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100,
    }

def clear_emoji_cache() -> None:  # pragma: no cover
    """
    Clears the logger name emoji lookup cache (`_EMOJI_LOOKUP_CACHE`).

    This function can be useful in testing environments to ensure a clean state
    for emoji prefixing tests or if a dynamic change in emoji configuration
    (not currently supported) would require cache invalidation.
    """
    global _EMOJI_LOOKUP_CACHE
    _EMOJI_LOOKUP_CACHE.clear()

# 🧱✨
