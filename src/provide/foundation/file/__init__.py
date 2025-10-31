#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.file.alignment import (
    CACHE_LINE_SIZE,
    DEFAULT_ALIGNMENT,
    PAGE_SIZE_4K,
    PAGE_SIZE_16K,
    align_offset,
    align_to_page,
    calculate_padding,
    get_system_page_size,
    is_aligned,
    is_power_of_two,
)
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
from provide.foundation.file.disk import (
    check_disk_space,
    format_bytes,
    get_available_space,
    get_disk_usage,
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
from provide.foundation.file.permissions import (
    DEFAULT_DIR_PERMS,
    DEFAULT_EXECUTABLE_PERMS,
    DEFAULT_FILE_PERMS,
    ensure_secure_permissions,
    format_permissions,
    get_permissions,
    parse_permissions,
    set_file_permissions,
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

"""File Operations Subsystem.

This module has a dual nature. It provides:
1. A rich set of standalone file utilities for safe and atomic operations,
   directory management, and format-specific helpers.
2. A framework component, OperationDetector, for analyzing file system
   events to identify logical operations like atomic saves.
"""

__all__ = [
    "CACHE_LINE_SIZE",
    "DEFAULT_ALIGNMENT",
    "DEFAULT_DIR_PERMS",
    "DEFAULT_EXECUTABLE_PERMS",
    "DEFAULT_FILE_PERMS",
    "PAGE_SIZE_4K",
    "PAGE_SIZE_16K",
    "DetectorConfig",
    "FileEvent",
    "FileEventMetadata",
    "FileLock",
    "FileOperation",
    "LockError",
    "OperationDetector",
    "OperationType",
    "align_offset",
    "align_to_page",
    "atomic_replace",
    "atomic_write",
    "atomic_write_text",
    "backup_file",
    "calculate_padding",
    "check_disk_space",
    "detect_atomic_save",
    "ensure_dir",
    "ensure_parent_dir",
    "ensure_secure_permissions",
    "extract_original_path",
    "find_files",
    "format_bytes",
    "format_permissions",
    "get_available_space",
    "get_disk_usage",
    "get_mtime",
    "get_permissions",
    "get_size",
    "get_system_page_size",
    "group_related_events",
    "is_aligned",
    "is_power_of_two",
    "is_temp_file",
    "parse_permissions",
    "read_json",
    "read_toml",
    "read_yaml",
    "safe_copy",
    "safe_delete",
    "safe_move",
    "safe_read",
    "safe_read_text",
    "safe_rmtree",
    "secure_temp_file",
    "set_file_permissions",
    "system_temp_dir",
    "temp_dir",
    "temp_file",
    "touch",
    "write_json",
    "write_toml",
    "write_yaml",
]

# 🧱🏗️🔚
