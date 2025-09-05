"""
Emoji-related type definitions for the Foundation logger.

This module contains data structures for emoji mapping configurations
used in structured logging visual enhancement.
"""

from attrs import define, field


@define(frozen=True, slots=True)
class CustomDasEmojiSet:
    """A named set of emojis for a specific category."""

    name: str = field()  # e.g., "component_types", "llm_operations", "request_outcomes"
    emojis: dict[str, str] = field(
        factory=lambda: {},
    )  # e.g., {"api": "🌐", "worker": "⚙️", "default": "🧩"}
    default_emoji_key: str = field(
        default="default"
    )  # The key within `emojis` to use as the default


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
    )  # Optional: references a CustomDasEmojiSet.name
    default_emoji_override_key: str | None = field(
        default=None
    )  # Optional: key within the emoji_set for this field's default


@define(frozen=True, slots=True)
class EmojiSet:
    """
    Simple emoji set for registry-based component management.
    
    This is used by the new component registry system for emoji management.
    """
    
    name: str = field()
    emojis: dict[str, str] = field(factory=lambda: {})


@define(frozen=True, slots=True)
class EmojiSetConfig:
    """
    Defines an emoji set configuration with emoji mappings for specific fields.
    Provides visual enhancement for structured logging in specific domains.
    """

    name: str = field()  # e.g., "llm", "database", "http_client"
    description: str | None = field(default=None)
    emoji_sets: list[CustomDasEmojiSet] = field(factory=lambda: [])
    field_definitions: list[FieldToEmojiMapping] = field(factory=lambda: [])
    priority: int = field(
        default=0, converter=int
    )  # Higher priority layers take precedence in case of conflicts
