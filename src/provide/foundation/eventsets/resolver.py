#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.eventsets.registry import get_registry
from provide.foundation.eventsets.types import EventMapping, FieldMapping

"""Event set resolution and enrichment logic."""


class EventSetResolver:
    """Resolves and applies event set enrichments to log events."""

    def __init__(self) -> None:
        """Initialize the resolver with cached configurations."""
        self._field_mappings: list[FieldMapping] = []
        self._event_mappings_by_set: dict[str, list[EventMapping]] = {}
        self._resolved = False

    def resolve(self) -> None:
        """Resolve all registered event sets into a unified configuration.

        This merges all registered event sets by priority, building
        the field mapping and event mapping lookup tables.
        """
        registry = get_registry()
        event_sets = registry.list_event_sets()  # Already sorted by priority

        # Clear existing state
        self._field_mappings.clear()
        self._event_mappings_by_set.clear()

        # Process each event set in priority order
        for event_set in event_sets:
            # Store event mappings by event set name
            self._event_mappings_by_set[event_set.name] = event_set.mappings

            # Add field mappings
            self._field_mappings.extend(event_set.field_mappings)

        self._resolved = True

    def _process_field_enrichment(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def _apply_visual_enrichments(self, enrichments: list[str], event_dict: dict[str, Any]) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get("event", "")
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def enrich_event(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def _find_event_mapping_for_field(self, field_key: str, field_value: Any) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def get_visual_markers(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers


# Global resolver instance
_resolver = EventSetResolver()


def get_resolver() -> EventSetResolver:
    """Get the global event set resolver instance."""
    return _resolver


def enrich_event(event_dict: dict[str, Any]) -> dict[str, Any]:
    """Enrich a log event with event set data.

    Args:
        event_dict: The event dictionary to enrich

    Returns:
        The enriched event dictionary

    """
    return _resolver.enrich_event(event_dict)


# 🧱🏗️🔚
