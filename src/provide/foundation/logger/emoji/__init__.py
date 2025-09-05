"""
Emoji configuration and mapping for Foundation logger.

This module provides emoji sets and mappings for visual enhancement
of structured logs in various domains (HTTP, LLM, Database, etc.).
"""

from provide.foundation.logger.emoji.matrix import (
    PRIMARY_EMOJI,
    SECONDARY_EMOJI,
    TERTIARY_EMOJI,
    show_emoji_matrix,
)
from provide.foundation.logger.emoji.sets import (
    DATABASE_EMOJI_SET,
    HTTP_EMOJI_SET,
    LEGACY_DAS_EMOJI_SETS,
    LEGACY_DAS_FIELD_DEFINITIONS,
    LLM_EMOJI_SET,
)
from provide.foundation.logger.emoji.types import (
    EmojiSet,
    EmojiSetConfig,
    FieldToEmojiMapping,
)

__all__ = [
    # Core emoji dictionaries
    "PRIMARY_EMOJI",
    "SECONDARY_EMOJI",
    "TERTIARY_EMOJI",
    # Emoji sets
    "DATABASE_EMOJI_SET",
    "HTTP_EMOJI_SET",
    "LLM_EMOJI_SET",
    "LEGACY_DAS_EMOJI_SETS",
    "LEGACY_DAS_FIELD_DEFINITIONS",
    # Types
    "EmojiSet",
    "EmojiSetConfig",
    "FieldToEmojiMapping",
    # Utilities
    "show_emoji_matrix",
]
