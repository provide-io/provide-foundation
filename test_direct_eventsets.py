#!/usr/bin/env python3
"""
Direct test of event sets types.
"""

import sys
sys.path.insert(0, "/Users/tim/code/gh/provide-io/provide-foundation/src")

# Direct import of event set files
from provide.foundation.eventsets.sets import das, http, database, llm, task_queue

def test():
    print("Testing event set definitions...")
    
    sets = [
        das.EVENT_SET,
        http.EVENT_SET,
        database.EVENT_SET,
        llm.EVENT_SET,
        task_queue.EVENT_SET
    ]
    
    for event_set in sets:
        print(f"\n{event_set.name} (priority: {event_set.priority})")
        print(f"  Description: {event_set.description}")
        print(f"  Field mappings: {len(event_set.field_mappings)}")
        print(f"  Event sets: {len(event_set.event_sets)}")
        
        # Show some visual markers
        if event_set.event_sets:
            es = event_set.event_sets[0]
            print(f"  Sample from '{es.name}':")
            for key, marker in list(es.visual_markers.items())[:3]:
                print(f"    {marker} -> {key}")

if __name__ == "__main__":
    test()