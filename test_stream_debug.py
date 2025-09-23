#!/usr/bin/env python3
"""Debug script for StreamManager timeout issue."""

import sys
import os

# Set PYTHONPATH
sys.path.insert(0, 'src')

# Disable Foundation logging to avoid initialization loops
os.environ['PROVIDE_LOG_LEVEL'] = 'CRITICAL'
os.environ['FOUNDATION_SUPPRESS_TESTING_WARNINGS'] = 'true'

def test_stream_manager_simple():
    """Test StreamManager creation without Foundation setup."""
    print("1. Importing StreamManager...")
    from provide.foundation.state.managers import StreamManager
    print("2. Creating default manager...")
    manager = StreamManager.create_default()
    print("3. Checking initial state...")
    print(f"   Log stream: {manager.current_log_stream}")
    print(f"   Is file open: {manager.is_file_open}")
    print("4. Setting mock stream...")
    from unittest.mock import Mock
    mock_stream = Mock()
    manager.set_log_stream(mock_stream)
    print(f"   New stream: {manager.current_log_stream}")
    print("5. Calling reset_to_default...")
    manager.reset_to_default()
    print("6. Reset completed successfully!")
    print(f"   Final stream: {manager.current_log_stream}")

if __name__ == "__main__":
    test_stream_manager_simple()