#!/usr/bin/env python3
"""
Simple test for event sets without logger.
"""

import sys
sys.path.insert(0, "/Users/tim/code/gh/provide-io/provide-foundation/src")

from provide.foundation.eventsets.registry import discover_event_sets, get_registry
from provide.foundation.eventsets.resolver import get_resolver

def test():
    print("Testing event sets...")
    
    # Discover sets
    discover_event_sets()
    
    # Get registry
    registry = get_registry()
    sets = registry.list_event_sets()
    
    print(f"Found {len(sets)} event sets:")
    for s in sets:
        print(f"  - {s.name} (priority: {s.priority})")
    
    # Test resolver
    resolver = get_resolver()
    resolver.resolve()
    
    # Test enrichment
    test_event = {
        "event": "Test message",
        "domain": "system",
        "action": "start",
        "status": "success"
    }
    
    enriched = resolver.enrich_event(test_event.copy())
    print(f"\nOriginal: {test_event}")
    print(f"Enriched: {enriched}")

if __name__ == "__main__":
    test()