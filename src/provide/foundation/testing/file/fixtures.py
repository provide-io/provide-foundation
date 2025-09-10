"""
File and Directory Test Fixtures.

Core file testing fixtures with re-exports from specialized modules.
Common fixtures for testing file operations, creating temporary directories,
and standard test file structures used across the provide-io ecosystem.
"""

# Re-export all fixtures from specialized modules
from provide.foundation.testing.file.directory_fixtures import (
    temp_directory,
    test_files_structure,
    nested_directory_structure, 
    empty_directory,
)

from provide.foundation.testing.file.special_fixtures import (
    binary_file,
    readonly_file,
    temp_symlink,
    temp_executable_file,
)

from provide.foundation.testing.file.content_fixtures import (
    temp_file,
    temp_named_file,
    temp_file_with_content,
    temp_binary_file,
    temp_csv_file,
    temp_json_file,
)


__all__ = [
    # Directory fixtures
    "temp_directory",
    "test_files_structure", 
    "nested_directory_structure",
    "empty_directory",
    # Special file fixtures
    "binary_file",
    "readonly_file",
    "temp_symlink",
    "temp_executable_file",
    # Content-based fixtures
    "temp_file",
    "temp_named_file",
    "temp_file_with_content", 
    "temp_binary_file",
    "temp_csv_file",
    "temp_json_file",
]