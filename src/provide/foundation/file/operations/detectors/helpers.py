"""Shared helper functions for file operation detectors."""

from __future__ import annotations

from pathlib import Path
import re


def is_temp_file(path: Path) -> bool:
    """Check if path looks like a temporary file."""
    name = path.name.lower()
    stem = path.stem.lower()

    # Common temp file patterns
    temp_patterns = [
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        ".$" in name,  # .$ prefix (common in Windows)
        stem.endswith(".tmp"),
        ".swp" in name,  # vim swap files
        ".swx" in name,  # vim swap files
        ".swo" in name,  # vim swap files
        ".#" in name,  # emacs temp files
        name.startswith("#") and name.endswith("#"),  # emacs autosave files
        name.endswith(".bak"),  # backup files
        name.endswith(".orig"),  # backup files
    ]

    return any(temp_patterns)


def is_backup_file(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def extract_base_name(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files: .document.txt.swp -> .document.txt
    vim_swap_pattern = r"\.(swp|swo|swx)$"
    if re.search(vim_swap_pattern, base_name):
        base_name = re.sub(vim_swap_pattern, "", base_name)
        return base_name if base_name and base_name != name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84
    base_name = re.sub(r"\.tmp\.\d+$", "", base_name)

    return base_name if base_name and base_name != name else None
