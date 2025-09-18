#!/usr/bin/env python3
"""Improved script to fix E402 import ordering violations while preserving conditional imports."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from typing import Any


def find_conditional_imports(content: str) -> list[tuple[int, int]]:
    """Find line ranges for conditional imports that should not be moved."""
    conditional_ranges = []
    lines = content.splitlines()

    # Common patterns that indicate conditional imports
    conditional_patterns = [
        r'try:',
        r'if\s+TYPE_CHECKING:',
        r'if\s+_HAS_',
        r'if\s+.*\bclick\b',
        r'if\s+.*\bcrypto\b',
    ]

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Check if this line starts a conditional block
        is_conditional = any(re.match(pattern, line) for pattern in conditional_patterns)

        if is_conditional:
            start_line = i
            # Find the end of the conditional block
            indent_level = len(lines[i]) - len(lines[i].lstrip())

            # Look for the end of this block
            j = i + 1
            while j < len(lines):
                current_line = lines[j]
                if current_line.strip() == "":
                    j += 1
                    continue

                current_indent = len(current_line) - len(current_line.lstrip())

                # If we've returned to the same or lower indent level and it's not an except/finally
                if current_indent <= indent_level:
                    if not re.match(r'\s*(except|finally|elif|else):', current_line):
                        break

                j += 1

            conditional_ranges.append((start_line, j - 1))
            i = j
        else:
            i += 1

    return conditional_ranges


def is_in_conditional_range(line_num: int, conditional_ranges: list[tuple[int, int]]) -> bool:
    """Check if a line number is within any conditional range."""
    return any(start <= line_num <= end for start, end in conditional_ranges)


def parse_imports_and_content(content: str) -> tuple[list[str], str, str, list[tuple[int, int]]]:
    """Parse file content to extract imports and remaining content."""
    lines = content.splitlines()

    # Find conditional import ranges first
    conditional_ranges = find_conditional_imports(content)

    # Find the __future__ import line (should be first)
    future_import_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('from __future__ import'):
            future_import_idx = i
            break

    if future_import_idx == -1:
        return [], "", content, conditional_ranges

    # Start collecting imports after the __future__ import and any blank lines
    import_start = future_import_idx + 1
    while import_start < len(lines) and not lines[import_start].strip():
        import_start += 1

    # Find docstring if it exists
    docstring = ""
    docstring_start = -1
    docstring_end = -1

    # Look for docstring (triple quotes)
    for i in range(import_start, len(lines)):
        line = lines[i].strip()
        if line.startswith('"""') or line.startswith("'''"):
            docstring_start = i
            # Find end of docstring
            quote_char = line[:3]
            if line.endswith(quote_char) and len(line) > 3:
                # Single line docstring
                docstring_end = i
            else:
                # Multi-line docstring
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().endswith(quote_char):
                        docstring_end = j
                        break
            break

    # Extract docstring if found
    if docstring_start != -1 and docstring_end != -1:
        docstring = '\n'.join(lines[docstring_start:docstring_end + 1])

    # Collect import lines and other non-import content
    import_lines = []
    remaining_lines = []

    i = import_start
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip docstring lines
        if docstring_start != -1 and docstring_start <= i <= docstring_end:
            i += 1
            continue

        # Skip conditional import blocks
        if is_in_conditional_range(i, conditional_ranges):
            remaining_lines.append(line)
            i += 1
            continue

        # Check if this is an import line (including multiline imports)
        if (stripped.startswith('import ') or
            stripped.startswith('from ') or
            (stripped == '' and i + 1 < len(lines) and
             (lines[i + 1].strip().startswith('import ') or lines[i + 1].strip().startswith('from ')))):

            # Handle multi-line imports
            import_block = []
            current_line = line
            import_block.append(current_line)

            # Check for continuation (parentheses)
            if '(' in current_line and ')' not in current_line:
                i += 1
                while i < len(lines):
                    import_block.append(lines[i])
                    if ')' in lines[i]:
                        break
                    i += 1

            # Add the import block
            import_lines.extend(import_block)
        else:
            # Non-import content
            remaining_lines.append(line)

        i += 1

    # Join the remaining content
    remaining_content = '\n'.join(remaining_lines)

    return import_lines, docstring, remaining_content, conditional_ranges


def categorize_imports(import_lines: list[str]) -> tuple[list[str], list[str], list[str]]:
    """Categorize imports into standard library, third-party, and local."""
    stdlib_imports = []
    third_party_imports = []
    local_imports = []

    stdlib_modules = {
        'abc', 'argparse', 'ast', 'asyncio', 'base64', 'bz2', 'collections',
        'contextlib', 'contextvars', 'copy', 'datetime', 'decimal', 'functools',
        'gzip', 'hashlib', 'hmac', 'http', 'io', 'itertools', 'json', 'logging',
        'math', 'multiprocessing', 'os', 'pathlib', 'pickle', 'platform', 're',
        'secrets', 'shutil', 'ssl', 'subprocess', 'sys', 'tarfile', 'tempfile',
        'threading', 'time', 'typing', 'urllib', 'uuid', 'warnings', 'weakref',
        'zipfile', 'zlib', 'builtins', 'configparser', 'csv', 'enum', 'fcntl',
        'getpass', 'importlib', 'inspect', 'operator', 'select', 'string',
        'textwrap', 'traceback'
    }

    current_block = []

    for line in import_lines:
        stripped = line.strip()
        if not stripped:
            if current_block:
                # Determine category of current block
                first_import = current_block[0].strip()
                if first_import.startswith('from '):
                    module = first_import.split()[1].split('.')[0]
                elif first_import.startswith('import '):
                    module = first_import.split()[1].split('.')[0]
                else:
                    module = ''

                if module.startswith('provide.'):
                    local_imports.extend(current_block)
                elif module in stdlib_modules:
                    stdlib_imports.extend(current_block)
                else:
                    third_party_imports.extend(current_block)

                current_block = []
            continue

        current_block.append(line)

    # Handle the last block
    if current_block:
        first_import = current_block[0].strip()
        if first_import.startswith('from '):
            module = first_import.split()[1].split('.')[0]
        elif first_import.startswith('import '):
            module = first_import.split()[1].split('.')[0]
        else:
            module = ''

        if module.startswith('provide.'):
            local_imports.extend(current_block)
        elif module in stdlib_modules:
            stdlib_imports.extend(current_block)
        else:
            third_party_imports.extend(current_block)

    return stdlib_imports, third_party_imports, local_imports


def fix_file_imports(file_path: Path) -> bool:
    """Fix import ordering in a single file."""
    try:
        content = file_path.read_text()

        # Skip files that don't have __future__ imports
        if 'from __future__ import annotations' not in content:
            return False

        import_lines, docstring, remaining, conditional_ranges = parse_imports_and_content(content)

        if not import_lines:
            return False

        # Categorize imports
        stdlib, third_party, local = categorize_imports(import_lines)

        # Build new content
        new_lines = ['from __future__ import annotations', '']

        # Add imports in order
        if stdlib:
            new_lines.extend([line for line in stdlib if line.strip()])
            new_lines.append('')

        if third_party:
            new_lines.extend([line for line in third_party if line.strip()])
            new_lines.append('')

        if local:
            new_lines.extend([line for line in local if line.strip()])
            new_lines.append('')

        # Add docstring if it exists
        if docstring:
            new_lines.append(docstring)
            new_lines.append('')

        # Add remaining content
        if remaining.strip():
            new_lines.append(remaining)

        new_content = '\n'.join(new_lines)

        # Only write if content changed
        if new_content.strip() != content.strip():
            file_path.write_text(new_content)
            return True

        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function to fix all Python files in src/ directory."""
    src_dir = Path("src")
    if not src_dir.exists():
        print("src/ directory not found")
        return 1

    fixed_count = 0
    total_count = 0

    for py_file in src_dir.rglob("*.py"):
        total_count += 1
        if fix_file_imports(py_file):
            fixed_count += 1
            print(f"Fixed: {py_file}")

    print(f"\nProcessed {total_count} files, fixed {fixed_count} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())