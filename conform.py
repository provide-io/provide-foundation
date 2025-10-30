#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A script to enforce header and footer conformance on Python files."""

import ast
import os
import sys
from typing import Optional, Tuple

# --- Protocol Constants ---

HEADER_SHEBANG = "#!/usr/bin/env python3"
HEADER_LIBRARY = "# "
SPDX_BLOCK = [
    "# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.",
    "# SPDX-License-Identifier: Apache-2.0",
    "#",
]
PLACEHOLDER_DOCSTRING = '"""TODO: Add module docstring."""'
FOOTER = "# 🧱🏗️🔚"

# --- Logic ---

def find_module_docstring_and_body_start(content: str) -> Tuple[Optional[str], int]:
    """
    Parses the Python source code to find the module-level docstring
    and the line number where the main body of the code starts.

    Returns:
        A tuple containing the docstring string (if found) and the
        1-based line number where the code body begins.
    """
    try:
        tree = ast.parse(content)
        docstring = ast.get_docstring(tree)

        if not tree.body:
            return docstring, len(content.splitlines()) + 1

        first_node = tree.body[0]
        start_lineno = first_node.lineno

        # If the first node is the docstring, the actual code starts after it.
        if isinstance(first_node, ast.Expr) and isinstance(first_node.value, ast.Str):
            if len(tree.body) > 1:
                # The "body" starts at the next node
                start_lineno = tree.body[1].lineno
            else:
                # The file ONLY contains a docstring
                start_lineno = len(content.splitlines()) + 1 # End of file

        return docstring, start_lineno
    except SyntaxError:
        # If the file is not valid Python, we can't parse it.
        # We'll treat it as having no docstring and starting at line 1.
        return None, 1


def conform_file(filepath: str) -> None:
    """
    Applies the header and footer protocol to a single Python file.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            content = "".join(lines)
    except (IOError, UnicodeDecodeError) as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return

    if not lines:
        # Handle empty files
        final_content = "\n".join([HEADER_LIBRARY] + SPDX_BLOCK) + "\n\n" + PLACEHOLDER_DOCSTRING + "\n\n" + FOOTER + "\n"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
        return


    # 1. Determine Header Type
    is_executable = lines[0].strip().startswith("#!")
    header_first_line = HEADER_SHEBANG if is_executable else HEADER_LIBRARY

    # 2. Preserve Docstring and find code body
    docstring, body_start_lineno = find_module_docstring_and_body_start(content)

    if docstring is None:
        docstring_str = PLACEHOLDER_DOCSTRING
    else:
        # Preserve original docstring formatting
        docstring_str = f'"""{docstring}"""'


    # 3. Extract the code body
    # The body is everything from the determined start line to the end,
    # minus any old footers.
    body_lines = lines[body_start_lineno - 1:]
    body_content = "".join(body_lines).rstrip()

    # Strip any old footers
    body_lines_stripped = body_content.splitlines()
    cleaned_body_lines = []
    for line in body_lines_stripped:
        if "🧱🏗️" not in line and "🐍🏗️" not in line:
            cleaned_body_lines.append(line)

    body_content = "\n".join(cleaned_body_lines).rstrip()


    # 4. Construct the new file content
    final_header = "\n".join([header_first_line] + SPDX_BLOCK)

    # Ensure there's content to separate from the footer
    if body_content:
        final_content = f"{final_header}\n\n{docstring_str}\n\n{body_content}\n\n{FOOTER}\n"
    else: # Handles files that might only have a docstring
        final_content = f"{final_header}\n\n{docstring_str}\n\n{FOOTER}\n"


    # 5. Write the conformed content back to the file
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
        # print(f"Conformed: {filepath}")
    except IOError as e:
        print(f"Error writing to file {filepath}: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python conform.py <file1.py> [file2.py] ...", file=sys.stderr)
        sys.exit(1)

    for filepath in sys.argv[1:]:
        if os.path.isfile(filepath) and filepath.endswith(".py"):
            conform_file(filepath)
        else:
            print(f"Skipping non-Python file or invalid path: {filepath}", file=sys.stderr)
