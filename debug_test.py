#!/usr/bin/env python3

import os
import sys

# Add the src directory to the path
sys.path.insert(0, '/Users/tim/code/gh/provide-io/provide-foundation/src')

# Set up testing environment
os.environ["CLICK_TESTING"] = "1"

print("Starting debug test...")

try:
    print("Importing reset function...")
    from provide.foundation.testing import reset_foundation_setup_for_testing
    
    print("Calling reset function...")
    reset_foundation_setup_for_testing()
    
    print("Reset completed successfully!")
    
except Exception as e:
    print(f"Error during reset: {e}")
    import traceback
    traceback.print_exc()

print("Test finished.")