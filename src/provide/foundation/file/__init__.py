"""File operations with safety, atomicity, and format support.

This module provides comprehensive file operations including:
- Atomic writes to prevent corruption
- Safe operations with error handling
- Directory management utilities
- Format-specific helpers for JSON, YAML, TOML
- File locking for concurrent access
- Various utility functions
"""

from provide.foundation.file.atomic import (
    atomic_replace,
    atomic_write,
    atomic_write_text,
)
from provide.foundation.file.directory import (
    ensure_dir,
    ensure_parent_dir,
    safe_rmtree,
    temp_dir,
)
from provide.foundation.file.formats import (
    read_json,
    read_toml,
    read_yaml,
    write_json,
    write_toml,
    write_yaml,
)
from provide.foundation.file.lock import FileLock, LockError
from provide.foundation.file.safe import (
    safe_copy,
    safe_delete,
    safe_move,
    safe_read,
    safe_read_text,
)
from provide.foundation.file.utils import (
    backup_file,
    find_files,
    get_mtime,
    get_size,
    touch,
)

__all__ = [
    # From atomic
    "atomic_write",
    "atomic_write_text",
    "atomic_replace",
    # From safe
    "safe_read",
    "safe_read_text",
    "safe_delete",
    "safe_move",
    "safe_copy",
    # From directory
    "ensure_dir",
    "ensure_parent_dir",
    "temp_dir",
    "safe_rmtree",
    # From formats
    "read_json",
    "write_json",
    "read_yaml",
    "write_yaml",
    "read_toml",
    "write_toml",
    # From lock
    "FileLock",
    "LockError",
    # From utils
    "get_size",
    "get_mtime",
    "touch",
    "find_files",
    "backup_file",
]