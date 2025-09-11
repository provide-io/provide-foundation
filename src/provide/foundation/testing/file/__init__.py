"""
File testing fixtures for the provide-io ecosystem.

Standard fixtures for file and directory operations that can be used
across any project that depends on provide.foundation.
"""

from provide.foundation.testing.file.fixtures import (
    binary_file,
    empty_directory,
    nested_directory_structure,
    readonly_file,
    temp_binary_file,
    temp_csv_file,
    temp_directory,
    temp_executable_file,
    temp_file,
    temp_file_with_content,
    temp_json_file,
    temp_named_file,
    temp_symlink,
    test_files_structure,
)

__all__ = [
    "binary_file",
    "empty_directory",
    "nested_directory_structure",
    "readonly_file",
    "temp_binary_file",
    "temp_csv_file",
    "temp_directory",
    "temp_executable_file",
    "temp_file",
    "temp_file_with_content",
    "temp_json_file",
    "temp_named_file",
    "temp_symlink",
    "test_files_structure",
]
