"""
Event set resolution and enrichment logic.
"""

from typing import Any

from provide.foundation.eventsets.registry import get_registry
from provide.foundation.eventsets.types import EventSet, EventSetConfig, FieldMapping


class EventSetResolver:
    """
    Resolves and applies event set enrichments to log events.
    """
    
    def __init__(self) -> None:
        """Initialize the resolver with cached configurations."""
        self._field_mappings: list[FieldMapping] = []
        self._event_sets: dict[str, EventSet] = {}
        self._resolved = False
    
    def resolve(self) -> None:
        """
        Resolve all registered event sets into a unified configuration.
        
        This merges all registered event sets by priority, building
        the field mapping and event set lookup tables.
        """
        registry = get_registry()
        configs = registry.list_event_sets()  # Already sorted by priority
        
        # Clear existing state
        self._field_mappings.clear()
        self._event_sets.clear()
        
        # Process each config in priority order
        for config in configs:
            # Add event sets to lookup
            for event_set in config.event_sets:
                if event_set.name not in self._event_sets:
                    self._event_sets[event_set.name] = event_set
            
            # Add field mappings
            self._field_mappings.extend(config.field_mappings)
        
        self._resolved = True
    
    def enrich_event(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """
        Enrich a log event with event set data.
        
        Args:
            event_dict: The event dictionary to enrich
            
        Returns:
            The enriched event dictionary
        """
        if not self._resolved:
            self.resolve()
        
        enrichments = []
        
        # Process each field mapping
        for mapping in self._field_mappings:
            if mapping.log_key not in event_dict:
                continue
            
            value = event_dict.get(mapping.log_key)
            if value is None:
                continue
            
            # Get the event set if specified
            if mapping.event_set_name and mapping.event_set_name in self._event_sets:
                event_set = self._event_sets[mapping.event_set_name]
                
                # Apply transformations
                value_str = str(value).lower()
                if value_str in event_set.transformations:
                    value = event_set.transformations[value_str](value)
                
                # Get visual marker
                default_key = mapping.default_override_key or event_set.default_key
                visual_marker = event_set.visual_markers.get(
                    value_str,
                    event_set.visual_markers.get(default_key, "")
                )
                
                if visual_marker:
                    enrichments.append(visual_marker)
                
                # Apply metadata fields
                if value_str in event_set.metadata_fields:
                    for meta_key, meta_value in event_set.metadata_fields[value_str].items():
                        if meta_key not in event_dict:
                            event_dict[meta_key] = meta_value
                
                # Remove the original field after processing
                event_dict.pop(mapping.log_key, None)
        
        # Add visual enrichments to event message
        if enrichments:
            prefix = "".join(f"[{e}]" for e in enrichments)
            event_msg = event_dict.get("event", "")
            event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix
        
        return event_dict
    
    def get_visual_markers(self, event_dict: dict[str, Any]) -> list[str]:
        """
        Extract visual markers for an event without modifying it.
        
        Args:
            event_dict: The event dictionary to analyze
            
        Returns:
            List of visual markers that would be applied
        """
        if not self._resolved:
            self.resolve()
        
        markers = []
        
        for mapping in self._field_mappings:
            if mapping.log_key not in event_dict:
                continue
            
            value = event_dict.get(mapping.log_key)
            if value is None:
                continue
            
            if mapping.event_set_name and mapping.event_set_name in self._event_sets:
                event_set = self._event_sets[mapping.event_set_name]
                value_str = str(value).lower()
                
                default_key = mapping.default_override_key or event_set.default_key
                marker = event_set.visual_markers.get(
                    value_str,
                    event_set.visual_markers.get(default_key, "")
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
    """
    Enrich a log event with event set data.
    
    Args:
        event_dict: The event dictionary to enrich
        
    Returns:
        The enriched event dictionary
    """
    return _resolver.enrich_event(event_dict)