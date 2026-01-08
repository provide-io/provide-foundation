#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from pathlib import Path
import re
import sys

EMOJI_MAP = {
    "archive": "📦",
    "cli": "💻",
    "concurrency": "🧵",
    "config": "⚙️",
    "console": "🖥️",
    "context": "🏷️",
    "crypto": "🔒",
    "docs": "📚",
    "errors": "🐛",
    "eventsets": "📊",
    "file": "📄",
    "formatting": "🎨",
    "hub": "🌐",
    "integrations": "🔌",
    "logger": "📝",
    "metrics": "📈",
    "observability": "🔭",
    "parsers": "🧩",
    "platform": "🏗️",
    "process": "🏃",
    "profiling": "⏱️",
    "resilience": "💪",
    "security": "🛡️",
    "serialization": "📜",
    "setup": "🛠️",
    "state": "💾",
    "streams": "🌊",
    "telemetry": "📡",
    "testmode": "🧪",
    "time": "🕰️",
    "tools": "🔧",
    "tracer": "👣",
    "transport": "🚚",
    "utils": "🧰",
    "default": "🤔",
}


def get_subsystem_emoji(filepath_str: str) -> str:
    """Gets the emoji for the subsystem based on the file path."""
    try:
        subsystem = filepath_str.split("/")[3]
        return EMOJI_MAP.get(subsystem, EMOJI_MAP["default"])
    except IndexError:
        return EMOJI_MAP["default"]


def modify_file(filepath_str) -> None:
    """
    This function modifies a file by replacing its header and adding an emoji line at the end.
    """
    filepath = Path(filepath_str)
    if not filepath.is_file():
        return

    with filepath.open() as f:
        lines = f.readlines()

    # Remove old emoji line if it exists
    lines = [line for line in lines if not re.match(r"^# .*", line.strip())]

    header_end_index = 0
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith("#"):
            header_end_index = i
            break
    else:  # all lines are comments or empty
        header_end_index = len(lines)

    has_existing_header = False
    if header_end_index > 0:
        header_content = "".join(lines[:header_end_index]).lower()
        if (
            "copyright" in header_content
            or "spdx-license-identifier" in header_content
            or "apache-2.0" in header_content
        ):
            has_existing_header = True

    content_lines = lines[header_end_index:] if has_existing_header else lines

    # Create new header
    try:
        relative_path = filepath.relative_to("src/provide/foundation")
        header_path = f"provide/foundation/{relative_path}"
    except ValueError:
        header_path = filepath_str

    header = [
        f"# {header_path}\n",
        "#\n",
        "# This is the provide.io LLC 2025 Copyright. All rights reserved.\n",
        "#\n",
        "# SPDX-License-Identifier: Apache-2.0\n",
        "\n",
    ]

    # Strip leading/trailing empty lines from content
    while content_lines and content_lines[0].strip() == "":
        content_lines.pop(0)
    while content_lines and content_lines[-1].strip() == "":
        content_lines.pop()

    subsystem_emoji = get_subsystem_emoji(filepath_str)
    emoji_line = f"\n\n# 🧱🤝{subsystem_emoji}🪄\n"

    new_content_lines = header + content_lines + [emoji_line]

    with filepath.open("w") as f:
        f.writelines(new_content_lines)


if __name__ == "__main__":
    for file_path in sys.argv[1:]:
        modify_file(file_path)

# 🧱🏗️🔚
