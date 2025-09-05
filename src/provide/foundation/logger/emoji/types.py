"""
Emoji-related type definitions for the Foundation logger.

This module contains data structures for emoji mapping configurations
used in structured logging visual enhancement.
"""

from attrs import define, field


@define(frozen=True, slots=True)
class EmojiSet:
    """
    Emoji set for registry-based component management.

    This replaces EmojiSet and is used by the new component registry system.
    """

    name: str = field()
    emojis: dict[str, str] = field(factory=lambda: {})
    default_emoji_key: str = field(default="default")


@define(frozen=True, slots=True)
class FieldToEmojiMapping:
    """
    Defines a single log field key and its optional emoji mapping.
    """

    log_key: str = field()  # e.g., "http.method", "llm.request.model"
    description: str | None = field(default=None)
    value_type: str | None = field(
        default=None
    )  # e.g., "string", "integer", "iso_timestamp"
    emoji_set_name: str | None = field(
        default=None
    )  # Optional: references an EmojiSet.name
    default_emoji_override_key: str | None = field(
        default=None
    )  # Optional: key within the emoji_set for this field's default


@define(frozen=True, slots=True)
class EmojiSetConfig:
    """
    Defines an emoji set configuration with emoji mappings for specific fields.
    Provides visual enhancement for structured logging in specific domains.
    """

    name: str = field()  # e.g., "llm", "database", "http_client"
    description: str | None = field(default=None)
    emoji_sets: list[EmojiSet] = field(factory=lambda: [])
    field_definitions: list[FieldToEmojiMapping] = field(factory=lambda: [])
    priority: int = field(
        default=0, converter=int
    )  # Higher priority layers take precedence in case of conflicts
