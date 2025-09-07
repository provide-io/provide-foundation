#!/usr/bin/env python3
"""
Final test of the refactored event sets system.
"""

import sys
import os
sys.path.insert(0, "/Users/tim/code/gh/provide-io/provide-foundation/src")

# Test environment setup
os.environ["PROVIDE_LOG_LEVEL"] = "DEBUG"
os.environ["PROVIDE_LOG_DAS_EMOJI_ENABLED"] = "true"

print("Testing final event sets system...")
print("=" * 50)

try:
    from provide.foundation.eventsets.registry import discover_event_sets, get_registry
    from provide.foundation.logger import get_logger
    
    # Test discovery
    print("1. Discovering event sets...")
    discover_event_sets()
    
    # Test registry
    registry = get_registry()
    event_sets = registry.list_event_sets()
    print(f"2. Found {len(event_sets)} event sets:")
    for es in event_sets:
        print(f"   - {es.name} (priority: {es.priority}, mappings: {len(es.mappings)})")
    
    # Test logger integration
    print("\n3. Testing logger integration:")
    logger = get_logger(__name__)
    
    # DAS test
    logger.info("Testing DAS", domain="system", action="start", status="success")
    
    print("\n✅ All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("=" * 50)