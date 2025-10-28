
import os
import sys
import ast

def get_module_docstring(source_code):
    """
    Parses Python source code and returns the module-level docstring.
    """
    try:
        tree = ast.parse(source_code)
        return ast.get_docstring(tree)
    except SyntaxError:
        return None

def conform_file(filepath):
    """
    Applies the header and footer protocol to a single Python file.
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()

    if not lines:
        return

    is_executable = lines[0].startswith('#!')

    # Preserve original docstring
    source_code = ''.join(lines)
    docstring = get_module_docstring(source_code)

    # Build the new header
    header = []
    if is_executable:
        header.append('#!/usr/bin/env python3\n')
    else:
        header.append('# \n')

    header.extend([
        '# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.\n',
        '# SPDX-License-Identifier: Apache-2.0\n',
        '#\n'
    ])

    if docstring:
        header.append(f'"""{docstring}"""\n')
    else:
        header.append('"""TODO: Add module docstring."""\n')

    # Find the start of the code (skip shebang, comments, and docstrings)
    code_start_index = 0
    in_docstring = False
    for i, line in enumerate(lines):
        if line.strip().startswith('#'):
            continue
        if '"""' in line or "'''" in line:
            in_docstring = not in_docstring
            if not in_docstring:
                code_start_index = i + 1
                break
            continue
        if not in_docstring and line.strip():
            code_start_index = i
            break

    # Combine header with the rest of the code
    new_content = "".join(header) + "\n" + "".join(lines[code_start_index:])

    # Remove old footers and trailing whitespace
    new_content = '\n'.join(line for line in new_content.split('\n') if '# 🧱🏗️' not in line and '# 🐍🏗️' not in line)
    new_content = new_content.rstrip()

    # Add new footer
    new_content += '\n\n# 🧱🏗️🔚\n'

    with open(filepath, 'w') as f:
        f.write(new_content)

if __name__ == "__main__":
    for filepath in sys.argv[1:]:
        conform_file(filepath)
