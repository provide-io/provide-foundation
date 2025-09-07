#
# emoji_resolver.py
#
"""
Emoji configuration resolution for Foundation Telemetry.
Handles the merging and resolution of emoji set configurations from multiple sources.
"""

from provide.foundation.logger.config import LoggingConfig
from provide.foundation.logger.emoji.sets import LEGACY_DAS_EMOJI_SETS
from provide.foundation.logger.emoji.types import (
    EmojiSet,
    EmojiSetConfig,
    FieldToEmojiMapping,
)

ResolvedEmojiConfig = tuple[list[FieldToEmojiMapping], dict[str, EmojiSet]]


def resolve_active_emoji_config(
    logging_config: LoggingConfig, builtin_emoji_registry: dict[str, EmojiSetConfig]
) -> ResolvedEmojiConfig:
    """
    Resolve the active emoji configuration from multiple sources.

    Args:
        logging_config: The logging configuration
        builtin_emoji_registry: Registry of built-in emoji sets

    Returns:
        Tuple of (field_definitions, emoji_sets_dict)
    """
    resolved_fields_dict: dict[str, FieldToEmojiMapping] = {}
    resolved_emoji_sets_dict: dict[str, EmojiSet] = {
        s.name: s for s in LEGACY_DAS_EMOJI_SETS
    }

    emoji_sets_to_process: list[EmojiSetConfig] = [
        builtin_emoji_registry[name]
        for name in logging_config.enabled_emoji_sets
        if name in builtin_emoji_registry
    ]
    emoji_sets_to_process.extend(logging_config.custom_emoji_sets)
    emoji_sets_to_process.sort(key=lambda emoji_set: emoji_set.priority)

    ordered_log_keys: list[str] = []
    seen_log_keys: set[str] = set()

    for emoji_set_config in emoji_sets_to_process:
        for emoji_set in emoji_set_config.emoji_sets:
            resolved_emoji_sets_dict[emoji_set.name] = emoji_set
        for field_def in emoji_set_config.field_definitions:
            resolved_fields_dict[field_def.log_key] = field_def
            if field_def.log_key not in seen_log_keys:
                ordered_log_keys.append(field_def.log_key)
                seen_log_keys.add(field_def.log_key)

    for user_emoji_set in logging_config.user_defined_emoji_sets:
        resolved_emoji_sets_dict[user_emoji_set.name] = user_emoji_set

    final_ordered_field_definitions = [
        resolved_fields_dict[log_key] for log_key in ordered_log_keys
    ]
    return final_ordered_field_definitions, resolved_emoji_sets_dict
