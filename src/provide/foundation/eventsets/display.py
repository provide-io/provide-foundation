"""
Event set display utilities for Foundation.
"""

from provide.foundation.logger import get_logger

from provide.foundation.eventsets.registry import get_registry, discover_event_sets
from provide.foundation.eventsets.resolver import get_resolver

logger = get_logger(__name__)


def show_event_matrix() -> None:
    """
    Display the active event set configuration to the console.
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
    if event_sets:
        lines.append(f"\nRegistered Event Sets ({len(event_sets)}):")
        for config in event_sets:
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
            
            # Show event sets
            if config.event_sets:
                lines.append(f"    Event Sets ({len(config.event_sets)}):")
                for event_set in config.event_sets:
                    marker_count = len(event_set.visual_markers)
                    metadata_count = len(event_set.metadata_fields)
                    transform_count = len(event_set.transformations)
                    lines.append(
                        f"      - {event_set.name}: "
                        f"{marker_count} markers, "
                        f"{metadata_count} metadata, "
                        f"{transform_count} transforms"
                    )
    else:
        lines.append("\n  (No event sets registered)")
    
    lines.append("\n" + "=" * 70)
    
    # Show resolved state
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_sets)}")
        
        # Show sample visual markers
        if resolver._event_sets:
            lines.append("\n  Sample Visual Markers:")
            for name, event_set in list(resolver._event_sets.items())[:3]:
                if event_set.visual_markers:
                    sample_markers = list(event_set.visual_markers.items())[:3]
                    lines.append(f"    {name}:")
                    for key, marker in sample_markers:
                        lines.append(f"      {marker} -> {key}")
    else:
        lines.append("\n  (Resolver not yet initialized)")
    
    # Log the complete display
    logger.info("\n".join(lines))