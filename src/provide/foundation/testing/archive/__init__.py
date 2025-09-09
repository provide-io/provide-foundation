"""
Archive testing fixtures for the provide-io ecosystem.

Standard fixtures for testing archive operations (tar, zip, gzip, bzip2)
across any project that depends on provide.foundation.
"""

from provide.foundation.testing.archive.fixtures import (
    archive_test_content,
    large_file_for_compression,
    multi_format_archives,
    archive_with_permissions,
    corrupted_archives,
    archive_stress_test_files,
)

__all__ = [
    "archive_test_content",
    "large_file_for_compression",
    "multi_format_archives",
    "archive_with_permissions",
    "corrupted_archives",
    "archive_stress_test_files",
]