#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""This script conforms Python files to a strict header/footer protocol."""

from __future__ import annotations

import ast
import sys

HEADER_SPDX = """# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#"""

FOOTER = "\n\n# 🧱🏗️🔚\n"
PLACEHOLDER_DOCSTRING = '"""TODO: Add module docstring."""'
OLD_FOOTERS = {"# 🧱🏗️🔚", "# 🐍🏗️🔚"}


def conform_file(filepath: str) -> None:
    """
    Reads a Python file, analyzes its structure, and rewrites it to conform
    to the specified header and footer protocol.
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
            lines = content.splitlines()
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return

    if not content.strip():
        return

    # 1. Analyze existing state
    is_executable = lines[0].startswith("#!") if lines else False

    docstring = None
    tree = None
    try:
        tree = ast.parse(content)
        docstring = ast.get_docstring(tree)
    except SyntaxError:
        print(f"Warning: Skipping file due to syntax error: {filepath}", file=sys.stderr)
        return

    # 2. Extract the code body
    body_content = ""
    if tree.body:
        first_node = tree.body[0]
        is_docstring_node = isinstance(first_node, ast.Expr) and isinstance(
            first_node.value, ast.Constant
        )

        start_node = None
        if is_docstring_node:
            if len(tree.body) > 1:
                start_node = tree.body[1]
        else:
            start_node = tree.body[0]

        if start_node:
            start_index = start_node.lineno - 1
            body_lines_list = lines[start_index:]
            body_content = "\n".join(body_lines_list)

    # 3. Clean the extracted body
    body_content = body_content.rstrip()
    if body_content:
        body_lines = body_content.splitlines()
        if body_lines and body_lines[-1].strip() in OLD_FOOTERS:
            body_lines = body_lines[:-1]
        final_body = "\n".join(body_lines).rstrip()
    else:
        final_body = ""

    # 4. Assemble new file content
    header_first_line = "#!/usr/bin/env python3" if is_executable else "#"
    final_header = f"{header_first_line}\n{HEADER_SPDX}\n"

    final_docstring = f'"""{docstring}"""' if docstring else PLACEHOLDER_DOCSTRING

    separator = "\n\n" if final_body else ""
    new_content = (
        f"{final_header}\n{final_docstring}{separator}{final_body}{FOOTER}"
    )

    # 5. Write back to file
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
    except OSError as e:
        print(f"Error writing to file {filepath}: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python conform.py <file1.py> <file2.py> ...", file=sys.stderr
        )
        sys.exit(1)

    for filepath in sys.argv[1:]:
        conform_file(filepath)

# 🧱🏗️🔚
