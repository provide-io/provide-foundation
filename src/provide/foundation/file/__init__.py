from __future__ import annotations

from provide.foundation.file.atomic import (
    atomic_replace,
    atomic_write,
    atomic_write_text,
)
from provide.foundation.file.directory import (
    ensure_dir,
    ensure_parent_dir,
    safe_rmtree,
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
from provide.foundation.file.operations import (
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    FileOperation,
    OperationDetector,
    OperationType,
    detect_atomic_save,
    extract_original_path,
    group_related_events,
    is_temp_file,
)
from provide.foundation.file.safe import (
    safe_copy,
    safe_delete,
    safe_move,
    safe_read,
    safe_read_text,
)
from provide.foundation.file.temp import secure_temp_file, system_temp_dir, temp_dir, temp_file
from provide.foundation.file.utils import (
    backup_file,
    find_files,
    get_mtime,
    get_size,
    touch,
)

"""File operations with safety, atomicity, and format support.

This module provides comprehensive file operations including:
- Atomic writes to prevent corruption
- Safe operations with error handling
- Directory management utilities
- Format-specific helpers for JSON, YAML, TOML
- File locking for concurrent access
- Various utility functions
"""

__all__ = [
    # From operations
    "DetectorConfig",
    "FileEvent",
    "FileEventMetadata",
    # From lock
    "FileLock",
    "FileOperation",
    "LockError",
    "OperationDetector",
    "OperationType",
    "atomic_replace",
    # From atomic
    "atomic_write",
    "atomic_write_text",
    "backup_file",
    "detect_atomic_save",
    # From directory
    "ensure_dir",
    "ensure_parent_dir",
    "extract_original_path",
    "find_files",
    "get_mtime",
    # From utils
    "get_size",
    "group_related_events",
    "is_temp_file",
    # From formats
    "read_json",
    "read_toml",
    "read_yaml",
    "safe_copy",
    "safe_delete",
    "safe_move",
    # From safe
    "safe_read",
    "safe_read_text",
    "safe_rmtree",
    # From temp
    "secure_temp_file",
    "system_temp_dir",
    "temp_dir",
    "temp_file",
    "touch",
    "write_json",
    "write_toml",
    "write_yaml",
]
