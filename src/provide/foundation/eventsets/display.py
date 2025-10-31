#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING

from provide.foundation.eventsets.registry import discover_event_sets, get_registry
from provide.foundation.eventsets.resolver import get_resolver
from provide.foundation.logger import get_logger

if TYPE_CHECKING:
    from provide.foundation.eventsets.resolver import EventSetResolver
    from provide.foundation.eventsets.types import EventSet

"""Event set display utilities for Foundation."""

log = get_logger(__name__)


def _format_event_set_config(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def _format_registered_event_sets(event_sets: list[EventSet], lines: list[str]) -> None:
    """Format the registered event sets section."""
    if event_sets:
        lines.append(f"\nRegistered Event Sets ({len(event_sets)}):")
        for config in event_sets:
            _format_event_set_config(config, lines)
    else:
        lines.append("\n  (No event sets registered)")


def _format_resolver_state(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def show_event_matrix() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


# 🧱🏗️🔚
