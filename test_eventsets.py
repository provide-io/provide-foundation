#!/usr/bin/env python3
"""
Test script for the new event sets system.
"""

import sys
import os

# Add foundation to path
sys.path.insert(0, "/Users/tim/code/gh/provide-io/provide-foundation/src")

# Set up logging to see the event sets in action
os.environ["PROVIDE_LOG_LEVEL"] = "DEBUG"
os.environ["PROVIDE_LOG_DAS_EMOJI_ENABLED"] = "true"

from provide.foundation.logger import get_logger
from provide.foundation.eventsets.registry import discover_event_sets, get_registry
from provide.foundation.eventsets.display import show_event_matrix

# Initialize logger
logger = get_logger(__name__)

def test_event_sets():
    """Test the event sets system."""
    
    print("=" * 70)
    print("Testing Event Sets System")
    print("=" * 70)
    
    # Discover and register all event sets
    print("\n1. Discovering event sets...")
    discover_event_sets()
    
    # List registered event sets
    registry = get_registry()
    event_sets = registry.list_event_sets()
    
    print(f"\n2. Found {len(event_sets)} event sets:")
    for config in event_sets:
        print(f"   - {config.name} (priority: {config.priority})")
    
    # Show the event matrix
    print("\n3. Displaying event matrix:")
    show_event_matrix()
    
    # Test logging with event enrichment
    print("\n4. Testing event enrichment in logs:")
    
    # Test DAS enrichment
    logger.info("Testing DAS enrichment", domain="system", action="start", status="success")
    
    # Test HTTP enrichment
    logger.info("HTTP request", **{
        "http.method": "get",
        "http.status_class": "2xx",
        "duration_ms": 150
    })
    
    # Test database enrichment
    logger.info("Database query", **{
        "db.system": "postgres",
        "db.operation": "select",
        "db.outcome": "success",
        "duration_ms": 25
    })
    
    # Test LLM enrichment
    logger.info("LLM interaction", **{
        "llm.provider": "anthropic",
        "llm.task": "chat",
        "llm.outcome": "success",
        "llm.input.tokens": 500,
        "llm.output.tokens": 1200
    })
    
    print("\n" + "=" * 70)
    print("Event Sets Test Complete")
    print("=" * 70)

if __name__ == "__main__":
    test_event_sets()