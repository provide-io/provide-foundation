"""
Event set type definitions for the Foundation event enrichment system.
"""

from collections.abc import Callable
from typing import Any

from attrs import define, field


@define(frozen=True, slots=True)
class EventSet:
    """
    A set of event enrichment mappings for a specific domain.
    
    Attributes:
        name: Unique identifier for this event set
        visual_markers: Mapping of values to visual indicators (e.g., emojis)
        metadata_fields: Additional metadata to attach based on values
        transformations: Value transformation functions
        default_key: Key to use when no specific match is found
    """
    
    name: str
    visual_markers: dict[str, str] = field(factory=lambda: {})
    metadata_fields: dict[str, dict[str, Any]] = field(factory=lambda: {})
    transformations: dict[str, Callable[[Any], Any]] = field(factory=lambda: {})
    default_key: str = field(default="default")


@define(frozen=True, slots=True)
class FieldMapping:
    """
    Maps a log field to an event set for enrichment.
    
    Attributes:
        log_key: The field key in log events (e.g., "http.method", "llm.provider")
        description: Human-readable description of this field
        value_type: Expected type of the field value
        event_set_name: Name of the EventSet to use for enrichment
        default_override_key: Override the default key for this specific field
    """
    
    log_key: str
    description: str | None = field(default=None)
    value_type: str | None = field(default=None)
    event_set_name: str | None = field(default=None)
    default_override_key: str | None = field(default=None)


@define(frozen=True, slots=True)
class EventSetConfig:
    """
    Configuration for a complete event enrichment domain.
    
    Attributes:
        name: Unique identifier for this configuration
        description: Human-readable description
        event_sets: List of EventSet definitions
        field_mappings: List of field-to-event-set mappings
        priority: Higher priority configs override lower ones
    """
    
    name: str
    description: str | None = field(default=None)
    event_sets: list[EventSet] = field(factory=lambda: [])
    field_mappings: list[FieldMapping] = field(factory=lambda: [])
    priority: int = field(default=0, converter=int)