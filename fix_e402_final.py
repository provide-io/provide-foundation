#!/usr/bin/env python3
"""Final E402 fix script that preserves conditional imports properly."""

import ast
import os
import re
from pathlib import Path
from typing import Any


class ImportReorganizer(ast.NodeVisitor):
    """AST visitor to reorganize imports and preserve conditional imports."""

    def __init__(self) -> None:
        self.imports_to_move: list[tuple[int, str]] = []
        self.conditional_blocks: list[tuple[int, int]] = []
        self.future_imports: list[tuple[int, str]] = []

    def visit_Try(self, node: ast.Try) -> Any:
        """Mark try blocks as conditional."""
        self.conditional_blocks.append((node.lineno, node.end_lineno or node.lineno))
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> Any:
        """Mark if blocks as conditional."""
        # Check if this is a TYPE_CHECKING block or other conditional imports
        if isinstance(node.test, ast.Name) and node.test.id == "TYPE_CHECKING":
            self.conditional_blocks.append((node.lineno, node.end_lineno or node.lineno))
        elif isinstance(node.test, ast.Attribute) and isinstance(node.test.value, ast.Name):
            # Handle patterns like _HAS_CLICK
            if node.test.value.id.startswith("_HAS_"):
                self.conditional_blocks.append((node.lineno, node.end_lineno or node.lineno))
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        """Mark function definitions as potential containers for conditional imports."""
        if node.name == "__getattr__":
            # This is likely lazy loading
            self.conditional_blocks.append((node.lineno, node.end_lineno or node.lineno))
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> Any:
        """Process import statements."""
        if not self._is_in_conditional_block(node.lineno):
            # Handle both 'aliases' and 'names' attributes for compatibility
            names_list = getattr(node, 'aliases', getattr(node, 'names', []))
            for alias in names_list:
                import_line = f"import {alias.name}"
                if getattr(alias, 'asname', None):
                    import_line += f" as {alias.asname}"
                self.imports_to_move.append((node.lineno, import_line))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        """Process from...import statements."""
        # Handle both 'aliases' and 'names' attributes for compatibility
        names_list = getattr(node, 'aliases', getattr(node, 'names', []))

        if node.module == "__future__":
            # Handle future imports specially
            for alias in names_list:
                import_line = f"from __future__ import {alias.name}"
                self.future_imports.append((node.lineno, import_line))
        elif not self._is_in_conditional_block(node.lineno):
            # Regular imports that should be moved
            module = node.module or ""
            names = []
            for alias in names_list:
                if getattr(alias, 'asname', None):
                    names.append(f"{alias.name} as {alias.asname}")
                else:
                    names.append(alias.name)
            import_line = f"from {module} import {', '.join(names)}"
            self.imports_to_move.append((node.lineno, import_line))
        self.generic_visit(node)

    def _is_in_conditional_block(self, lineno: int) -> bool:
        """Check if a line is within a conditional block."""
        for start, end in self.conditional_blocks:
            if start <= lineno <= end:
                return True
        return False


def categorize_imports(imports: list[str]) -> tuple[list[str], list[str], list[str]]:
    """Categorize imports into stdlib, third-party, and local."""
    stdlib_modules = {
        'abc', 'argparse', 'asyncio', 'base64', 'builtins', 'collections', 'configparser',
        'contextlib', 'copy', 'datetime', 'decimal', 'enum', 'fcntl', 'functools', 'getpass',
        'hashlib', 'importlib', 'io', 'itertools', 'json', 'logging', 'math', 'multiprocessing',
        'os', 'pathlib', 'pickle', 'platform', 'random', 're', 'select', 'shutil', 'signal',
        'socket', 'sqlite3', 'subprocess', 'sys', 'tempfile', 'textwrap', 'threading', 'time',
        'traceback', 'typing', 'urllib', 'uuid', 'warnings', 'weakref', 'xml', 'zipfile'
    }

    stdlib_imports = []
    third_party_imports = []
    local_imports = []

    for import_line in imports:
        # Extract the module name
        if import_line.startswith("from "):
            module = import_line.split()[1]
        else:  # import statement
            module = import_line.split()[1].split('.')[0]

        # Remove "as" aliases for categorization
        module = module.split(' as ')[0]

        if module.split('.')[0] in stdlib_modules:
            stdlib_imports.append(import_line)
        elif module.startswith('provide.'):
            local_imports.append(import_line)
        else:
            third_party_imports.append(import_line)

    return sorted(stdlib_imports), sorted(third_party_imports), sorted(local_imports)


def fix_e402_in_file(file_path: Path) -> bool:
    """Fix E402 violations in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')

        # Parse the AST to identify imports and conditional blocks
        try:
            tree = ast.parse(content)
        except SyntaxError:
            print(f"Syntax error in {file_path}, skipping")
            return False

        reorganizer = ImportReorganizer()
        reorganizer.visit(tree)

        # If no imports to move, skip
        if not reorganizer.imports_to_move:
            return False

        # Remove the imports that need to be moved
        lines_to_remove = {lineno - 1 for lineno, _ in reorganizer.imports_to_move}  # Convert to 0-based
        filtered_lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]

        # Find where to insert the reorganized imports
        insert_index = 0

        # Skip future imports
        for i, line in enumerate(filtered_lines):
            if line.strip().startswith('from __future__ import'):
                insert_index = i + 1
            elif line.strip() == '' and i <= 5:  # Allow some blank lines after future imports
                continue
            elif line.strip().startswith('#') and i <= 10:  # Allow some comments at top
                continue
            elif line.strip().startswith('"""') or line.strip().startswith("'''"):
                # Skip docstrings - find the end
                if line.strip() == '"""' or line.strip() == "'''":
                    quote = line.strip()
                    for j in range(i + 1, len(filtered_lines)):
                        if filtered_lines[j].strip() == quote:
                            insert_index = j + 1
                            break
                elif line.count('"""') == 2 or line.count("'''") == 2:
                    # Single line docstring
                    insert_index = i + 1
                else:
                    # Multi-line docstring start
                    quote = '"""' if '"""' in line else "'''"
                    for j in range(i + 1, len(filtered_lines)):
                        if quote in filtered_lines[j]:
                            insert_index = j + 1
                            break
                break
            else:
                break

        # Categorize and organize imports
        import_lines = [import_line for _, import_line in reorganizer.imports_to_move]
        stdlib_imports, third_party_imports, local_imports = categorize_imports(import_lines)

        # Build the new import section
        new_imports = []
        if stdlib_imports:
            new_imports.extend(stdlib_imports)
            new_imports.append('')
        if third_party_imports:
            new_imports.extend(third_party_imports)
            new_imports.append('')
        if local_imports:
            new_imports.extend(local_imports)
            new_imports.append('')

        # Remove the last empty line if present
        if new_imports and new_imports[-1] == '':
            new_imports.pop()

        # Insert the reorganized imports
        new_lines = (
            filtered_lines[:insert_index] +
            new_imports +
            ([''] if new_imports else []) +  # Add blank line after imports
            filtered_lines[insert_index:]
        )

        # Join and write back
        new_content = '\n'.join(new_lines)

        # Only write if content changed
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True

        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Fix E402 violations in all Python files."""
    src_dir = Path("src")
    if not src_dir.exists():
        print("src/ directory not found")
        return

    fixed_count = 0
    total_count = 0

    for py_file in src_dir.rglob("*.py"):
        total_count += 1
        if fix_e402_in_file(py_file):
            fixed_count += 1
            print(f"Fixed E402 in: {py_file}")

    print(f"\nFixed E402 in {fixed_count} of {total_count} Python files")


if __name__ == "__main__":
    main()