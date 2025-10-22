#!/usr/bin/env python3
"""Script to split large test files into smaller ones.

This script identifies test files over 500 LOC and splits them
into smaller, more manageable files based on test classes.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


def find_test_class_boundaries(content: str) -> list[tuple[int, str, int]]:
    """Find all test class definitions and their line ranges.

    Returns list of (start_line, class_name, approx_end_line) tuples.
    """
    lines = content.split("\n")
    classes = []

    for i, line in enumerate(lines, 1):
        if re.match(r"^class Test\w+", line):
            class_name = re.findall(r"class (Test\w+)", line)[0]
            classes.append((i, class_name))

    # Calculate end lines (next class start or EOF)
    class_ranges = []
    for idx, (start, name) in enumerate(classes):
        if idx + 1 < len(classes):
            end = classes[idx + 1][0] - 1
        else:
            end = len(lines)
        class_ranges.append((start, name, end))

    return class_ranges


def split_test_file(file_path: Path, target_lines: int = 400) -> list[Path]:
    """Split a test file into multiple files based on test classes.

    Args:
        file_path: Path to the test file to split
        target_lines: Target maximum lines per output file

    Returns:
        List of created file paths
    """
    content = file_path.read_text()
    lines = content.split("\n")

    # Find imports and module docstring (header)
    header_end = 0
    in_docstring = False
    for i, line in enumerate(lines):
        if line.strip().startswith('"""') and not in_docstring:
            in_docstring = True
            if line.count('"""') == 2:  # Single-line docstring
                in_docstring = False
        elif '"""' in line and in_docstring:
            in_docstring = False
            header_end = i + 1
        elif not in_docstring and (line.startswith("import ") or line.startswith("from ") or line.strip() == ""):
            header_end = i + 1
        elif not in_docstring and line and not line.startswith("#"):
            break

    header = "\n".join(lines[:header_end])

    # Find test classes
    class_ranges = find_test_class_boundaries(content)

    if not class_ranges:
        print(f"No test classes found in {file_path}")
        return []

    # Group classes into output files
    groups: list[list[tuple[int, str, int]]] = []
    current_group: list[tuple[int, str, int]] = []
    current_lines = 0

    for start, name, end in class_ranges:
        class_lines = end - start + 1

        if current_lines + class_lines > target_lines and current_group:
            groups.append(current_group)
            current_group = [(start, name, end)]
            current_lines = class_lines
        else:
            current_group.append((start, name, end))
            current_lines += class_lines

    if current_group:
        groups.append(current_group)

    # Create output files
    base_name = file_path.stem  # Remove .py
    created_files = []

    for idx, group in enumerate(groups, 1):
        # Generate descriptive name from class names
        class_names = [name.replace("Test", "").lower() for _, name, _ in group]
        suffix = "_".join(class_names[:2])  # Use first 2 class names
        if len(class_names) > 2:
            suffix += "_etc"

        output_name = f"{base_name}_{suffix}.py"
        output_path = file_path.parent / output_name

        # Build content
        output_lines = [header, ""]

        for start, name, end in group:
            # Extract class content (0-indexed)
            class_content = "\n".join(lines[start-1:end])
            output_lines.append(class_content)
            output_lines.append("")  # Blank line between classes

        output_path.write_text("\n".join(output_lines))
        created_files.append(output_path)
        print(f"  Created: {output_path.name} ({len(output_lines)} lines)")

    return created_files


def format_file(file_path: Path) -> None:
    """Run ruff format on a file."""
    subprocess.run(["ruff", "check", "--fix", "--unsafe-fixes", str(file_path)], check=False)
    subprocess.run(["ruff", "format", str(file_path)], check=False)


def main() -> None:
    """Main entry point."""
    test_files = [
        "tests/transport/test_client.py",
        "tests/hub/test_hub_nested_commands.py",
        "tests/config/test_config_manager_coverage.py",
        "tests/console/test_console_output_coverage.py",
        "tests/errors/test_handlers.py",
        "tests/integrations/openobserve/test_commands_unit.py",
        "tests/concurrency/test_async_core.py",
        "tests/file/test_file_quality_qualityanalyzer.py",
    ]

    repo_root = Path("/Users/tim/code/gh/provide-io/provide-foundation")

    for test_file in test_files:
        file_path = repo_root / test_file
        if not file_path.exists():
            print(f"Skipping {test_file} (already processed or not found)")
            continue

        line_count = len(file_path.read_text().split("\n"))
        print(f"\nProcessing: {test_file} ({line_count} lines)")

        # Split the file
        created_files = split_test_file(file_path)

        if created_files:
            # Format all created files
            for new_file in created_files:
                print(f"  Formatting: {new_file.name}")
                format_file(new_file)

            # Remove original file
            file_path.unlink()
            print(f"  Removed original: {file_path.name}")


if __name__ == "__main__":
    main()
