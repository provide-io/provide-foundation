#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# custom_processors.py
#
import logging as stdlib_logging
from typing import Any, Protocol

import structlog

from provide.foundation.logger.constants import DEFAULT_FALLBACK_NUMERIC
from provide.foundation.logger.levels import get_numeric_level, normalize_level
from provide.foundation.logger.types import TRACE_LEVEL_NAME, TRACE_LEVEL_NUM, LogLevelStr

"""Foundation Telemetry Custom Structlog Processors.
Includes processors for log level normalization, level-based filtering,
and logger name emoji prefixes. The semantic field emoji prefix processor
is now created as a closure in config.py.
"""

_NUMERIC_TO_LEVEL_NAME_CUSTOM: dict[int, str] = {
    stdlib_logging.CRITICAL: "critical",
    stdlib_logging.ERROR: "error",
    stdlib_logging.WARNING: "warning",
    stdlib_logging.INFO: "info",
    stdlib_logging.DEBUG: "debug",
    TRACE_LEVEL_NUM: TRACE_LEVEL_NAME.lower(),
}


class StructlogProcessor(Protocol):
    def __call__(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict: ...  # pragma: no cover


def add_log_level_custom(
    _logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    level_hint: str | None = event_dict.pop("_foundation_level_hint", None)
    if level_hint is not None:
        event_dict["level"] = level_hint.lower()
    elif "level" not in event_dict:
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
    def __init__(
        self,
        default_level_str: LogLevelStr,
        module_levels: dict[str, LogLevelStr],
        level_to_numeric_map: dict[LogLevelStr, int],
    ) -> None:
        self.default_numeric_level: int = level_to_numeric_map[default_level_str]
        self.module_numeric_levels: dict[str, int] = {
            module: level_to_numeric_map[level_str] for module, level_str in module_levels.items()
        }
        self.level_to_numeric_map = level_to_numeric_map
        self.sorted_module_paths: list[str] = sorted(self.module_numeric_levels.keys(), key=len, reverse=True)

    def __call__(
        self,
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        logger_name: str = event_dict.get("logger_name", "unnamed_filter_target")
        event_level_str_from_dict = str(event_dict.get("level", "info"))

        # Normalize the level and get numeric value safely
        normalized_level = normalize_level(event_level_str_from_dict)
        event_num_level: int = get_numeric_level(
            normalized_level,
            fallback=DEFAULT_FALLBACK_NUMERIC,
        )
        threshold_num_level: int = self.default_numeric_level
        for path_prefix in self.sorted_module_paths:
            if logger_name.startswith(path_prefix):
                threshold_num_level = self.module_numeric_levels[path_prefix]
                break
        if event_num_level < threshold_num_level:
            raise structlog.DropEvent
        return event_dict


def filter_by_level_custom(
    default_level_str: LogLevelStr,
    module_levels: dict[str, LogLevelStr],
    level_to_numeric_map: dict[LogLevelStr, int],
) -> _LevelFilter:
    return _LevelFilter(default_level_str, module_levels, level_to_numeric_map)


_LOGGER_NAME_EMOJI_PREFIXES: dict[str, str] = {
    "provide.foundation.core_setup": "🛠️",
    "provide.foundation.emoji_matrix_display": "💡",
    "provide.foundation.logger": "📝",
    "provide.foundation.logger.config": "🔩",
    "pyvider.dynamic_call_trace": "👣",
    "pyvider.dynamic_call": "🗣️",
    "formatter.test": "🎨",
    "service.alpha": "🇦",
    "service.beta": "🇧",
    "service.beta.child": "👶",
    "service.gamma.trace_enabled": "🇬",
    "service.delta": "🇩",
    "das.test": "🃏",
    "json.exc.test": "💥",
    "service.name.test": "📛",
    "unknown": "❓",
    "default": "🔹",
    "emoji.test": "🎭",
}
_SORTED_LOGGER_NAME_EMOJI_KEYWORDS: list[str] = sorted(
    _LOGGER_NAME_EMOJI_PREFIXES.keys(),
    key=len,
    reverse=True,
)
_EMOJI_LOOKUP_CACHE: dict[str, str] = {}
_EMOJI_CACHE_SIZE_LIMIT: int = 1000


def _compute_emoji_for_logger_name(logger_name: str) -> str:
    # Original keyword-based system
    for keyword in _SORTED_LOGGER_NAME_EMOJI_KEYWORDS:
        if keyword == "default":
            continue
        if logger_name.startswith(keyword):
            return _LOGGER_NAME_EMOJI_PREFIXES[keyword]
    return _LOGGER_NAME_EMOJI_PREFIXES.get("default", "🔹")


def add_logger_name_emoji_prefix(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    logger_name = event_dict.get("logger_name", "default")
    if logger_name in _EMOJI_LOOKUP_CACHE:
        chosen_emoji = _EMOJI_LOOKUP_CACHE[logger_name]
    else:
        chosen_emoji = _compute_emoji_for_logger_name(logger_name)
        if len(_EMOJI_LOOKUP_CACHE) < _EMOJI_CACHE_SIZE_LIMIT:
            _EMOJI_LOOKUP_CACHE[logger_name] = chosen_emoji
    event_msg = event_dict.get("event")
    if event_msg is not None:
        event_dict["event"] = f"{chosen_emoji} {event_msg}"
    elif chosen_emoji:
        event_dict["event"] = chosen_emoji
    return event_dict


def get_emoji_cache_stats() -> dict[str, Any]:  # pragma: no cover
    return {
        "cache_size": len(_EMOJI_LOOKUP_CACHE),
        "cache_limit": _EMOJI_CACHE_SIZE_LIMIT,
        "cache_utilization": len(_EMOJI_LOOKUP_CACHE) / _EMOJI_CACHE_SIZE_LIMIT * 100
        if _EMOJI_CACHE_SIZE_LIMIT > 0
        else 0,
    }


def clear_emoji_cache() -> None:  # pragma: no cover
    global _EMOJI_LOOKUP_CACHE
    _EMOJI_LOOKUP_CACHE.clear()


# 🧱🏗️🔚
