#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for file operation defaults - temp files, directories, and atomic writes."""

from provide.testkit import FoundationTestCase

from provide.foundation.config.defaults import (
    DEFAULT_ATOMIC_ENCODING,
    DEFAULT_ATOMIC_MODE,
    DEFAULT_DIR_MODE,
    DEFAULT_DIR_PARENTS,
    DEFAULT_MISSING_OK,
    DEFAULT_TEMP_CLEANUP,
    DEFAULT_TEMP_PREFIX,
    DEFAULT_TEMP_SUFFIX,
    DEFAULT_TEMP_TEXT_MODE,
)


class TestTempFileDefaults(FoundationTestCase):
    """Test temporary file/directory defaults."""

    def test_temp_file_defaults(self) -> None:
        """Test temporary file defaults."""
        assert DEFAULT_TEMP_PREFIX == "provide_"
        assert DEFAULT_TEMP_SUFFIX == ""
        assert DEFAULT_TEMP_CLEANUP is True
        assert DEFAULT_TEMP_TEXT_MODE is False

        assert isinstance(DEFAULT_TEMP_PREFIX, str)
        assert isinstance(DEFAULT_TEMP_SUFFIX, str)
        assert isinstance(DEFAULT_TEMP_CLEANUP, bool)
        assert isinstance(DEFAULT_TEMP_TEXT_MODE, bool)


class TestDirectoryDefaults(FoundationTestCase):
    """Test directory operation defaults."""

    def test_directory_defaults(self) -> None:
        """Test directory operation defaults."""
        assert DEFAULT_DIR_MODE == 0o755
        assert DEFAULT_DIR_PARENTS is True
        assert DEFAULT_MISSING_OK is True

        assert isinstance(DEFAULT_DIR_MODE, int)
        assert isinstance(DEFAULT_DIR_PARENTS, bool)
        assert isinstance(DEFAULT_MISSING_OK, bool)

    def test_directory_mode_validity(self) -> None:
        """Test directory mode is valid octal."""
        # Should be a valid file mode
        assert 0o000 <= DEFAULT_DIR_MODE <= 0o777


class TestAtomicWriteDefaults(FoundationTestCase):
    """Test atomic write defaults."""

    def test_atomic_write_defaults(self) -> None:
        """Test atomic write defaults."""
        assert DEFAULT_ATOMIC_MODE == 0o644
        assert DEFAULT_ATOMIC_ENCODING == "utf-8"

        assert isinstance(DEFAULT_ATOMIC_MODE, int)
        assert isinstance(DEFAULT_ATOMIC_ENCODING, str)

    def test_atomic_mode_validity(self) -> None:
        """Test atomic write mode is valid octal."""
        # Should be a valid file mode
        assert 0o000 <= DEFAULT_ATOMIC_MODE <= 0o777

    def test_atomic_encoding_validity(self) -> None:
        """Test atomic write encoding is valid."""
        # Should be a valid Python encoding
        "test".encode(DEFAULT_ATOMIC_ENCODING)


# 🧱🏗️🔚
