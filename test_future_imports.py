#!/usr/bin/env python3
"""
Test script to check which __future__ imports are actually needed.
"""

import subprocess
import sys
from pathlib import Path

# Files to test
files_to_test = [
    "src/provide/foundation/config/schema.py",
    "src/provide/foundation/config/manager.py", 
    "src/provide/foundation/config/env.py",
    "src/provide/foundation/hub/manager.py"
]

def test_import_removal(file_path):
    """Test if removing __future__ import breaks the file."""
    print(f"\nTesting {file_path}...")
    
    # Read current content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if it has the import
    if 'from __future__ import annotations' not in content:
        print(f"  ✅ No __future__ import found")
        return True
    
    # Remove the import temporarily
    modified_content = content.replace('from __future__ import annotations\n', '')
    
    # Write modified content
    with open(file_path, 'w') as f:
        f.write(modified_content)
    
    try:
        # Test import
        module_name = file_path.replace('src/', '').replace('/', '.').replace('.py', '')
        result = subprocess.run([
            sys.executable, '-c', 
            f'import {module_name}; print("  ✅ Works without __future__")'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"  ✅ {file_path} works without __future__")
            return True
        else:
            print(f"  ❌ {file_path} NEEDS __future__:")
            print(f"     {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error testing {file_path}: {e}")
        return False
    finally:
        # Restore original content
        with open(file_path, 'w') as f:
            f.write(content)

if __name__ == "__main__":
    print("Testing which __future__ imports are actually needed...\n")
    
    for file_path in files_to_test:
        needs_future = not test_import_removal(file_path)
        
    print("\nDone!")