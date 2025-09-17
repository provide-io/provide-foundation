#!/usr/bin/env python3
"""Fix broken import statements where docstrings interrupt imports."""

import os
import re
from pathlib import Path

def fix_broken_imports(file_path):
    """Fix broken imports in a single file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match: from ... import (\n\n"""docstring..."""\n\n    import_items...)
    pattern = r'(from\s+[\w.]+\s+import\s*\(\s*)\n\n(""".*?"""\s*)\n\n(\s+[\w,\s#\n_]+\))'

    def replacer(match):
        from_part = match.group(1)
        docstring = match.group(2)
        imports_part = match.group(3)

        # Reconstruct properly: from ... import (\n    items\n)\n\ndocstring
        return f"{from_part}\n{imports_part}\n\n{docstring}"

    fixed_content = re.sub(pattern, replacer, content, flags=re.DOTALL)

    if fixed_content != content:
        print(f"Fixing {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        return True
    return False

def main():
    """Find and fix all broken import files."""
    src_dir = Path("src")
    fixed_count = 0

    for py_file in src_dir.rglob("*.py"):
        if fix_broken_imports(py_file):
            fixed_count += 1

    print(f"Fixed {fixed_count} files")

if __name__ == "__main__":
    main()