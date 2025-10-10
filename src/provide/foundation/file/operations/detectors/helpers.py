"""Shared helper functions for file operation detectors."""

from __future__ import annotations

from pathlib import Path
import re


def is_temp_file(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    stem = path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),

        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),

        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),

        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),

        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files

        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
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

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

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

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None
