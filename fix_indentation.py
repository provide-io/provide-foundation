#!/usr/bin/env python3
"""Fix indentation issues in Python files caused by import fixing script."""

import os
import re
from pathlib import Path


def fix_indentation_in_file(file_path: Path) -> bool:
    """Fix indentation issues in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            # Fix imports that are incorrectly indented
            if re.match(r'^    (import |from \w)', line):
                # Remove the 4-space indent for imports that should be at module level
                fixed_lines.append(line[4:])
            elif re.match(r'^        (import |from \w)', line):
                # Remove the 8-space indent for imports that should be at module level
                fixed_lines.append(line[8:])
            elif re.match(r'^            (import |from \w)', line):
                # Remove the 12-space indent for imports that should be at module level
                fixed_lines.append(line[12:])
            elif re.match(r'^                (import |from \w)', line):
                # Remove the 16-space indent for imports that should be at module level
                fixed_lines.append(line[16:])
            else:
                fixed_lines.append(line)

        new_content = '\n'.join(fixed_lines)

        # Only write if content changed
        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Fix indentation issues in all Python files."""
    src_dir = Path("src")
    if not src_dir.exists():
        print("src/ directory not found")
        return

    fixed_count = 0
    total_count = 0

    for py_file in src_dir.rglob("*.py"):
        total_count += 1
        if fix_indentation_in_file(py_file):
            fixed_count += 1
            print(f"Fixed indentation in: {py_file}")

    print(f"\nFixed indentation in {fixed_count} of {total_count} Python files")


if __name__ == "__main__":
    main()