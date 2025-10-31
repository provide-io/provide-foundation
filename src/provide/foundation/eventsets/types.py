#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from attrs import define, field

from provide.foundation.config.defaults import DEFAULT_EVENT_KEY

"""Event set type definitions for the Foundation event enrichment system."""


@define(frozen=True, slots=True)
class EventMapping:
    """Individual event enrichment mapping for a specific domain.

    Attributes:
        name: Unique identifier for this mapping
        visual_markers: Mapping of values to visual indicators (e.g., emojis)
        metadata_fields: Additional metadata to attach based on values
        transformations: Value transformation functions
        default_key: Key to use when no specific match is found

    """

    name: str
    visual_markers: dict[str, str] = field(factory=dict)
    metadata_fields: dict[str, dict[str, Any]] = field(factory=dict)
    transformations: dict[str, Callable[[Any], Any]] = field(factory=dict)
    default_key: str = field(default=DEFAULT_EVENT_KEY)


@define(frozen=True, slots=True)
class FieldMapping:
    """Maps a log field to an event set for enrichment.

    Attributes:
        log_key: The field key in log events (e.g., "http.method", "llm.provider")
        description: Human-readable description of this field
        value_type: Expected type of the field value
        event_set_name: Name of the EventSet to use for enrichment
        default_override_key: Override the default key for this specific field
        default_value: Default value to use if field is not present

    """

    log_key: str
    description: str | None = field(default=None)
    value_type: str | None = field(default=None)
    event_set_name: str | None = field(default=None)
    default_override_key: str | None = field(default=None)
    default_value: Any | None = field(default=None)


@define(frozen=True, slots=True)
class EventSet:
    """Complete event enrichment domain definition.

    Attributes:
        name: Unique identifier for this event set
        description: Human-readable description
        mappings: List of EventMapping definitions
        field_mappings: List of field-to-mapping associations
        priority: Higher priority sets override lower ones

    """

    name: str
    description: str | None = field(default=None)
    mappings: list[EventMapping] = field(factory=list)
    field_mappings: list[FieldMapping] = field(factory=list)
    priority: int = field(default=0, converter=int)


# 🧱🏗️🔚
