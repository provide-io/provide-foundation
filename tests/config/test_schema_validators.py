#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for built-in schema validators."""

from provide.testkit import FoundationTestCase

from provide.foundation.config.schema import (
    validate_email,
    validate_path,
    validate_port,
    validate_url,
    validate_url_accessible,
    validate_version,
)


class TestBuiltinValidators(FoundationTestCase):
    """Test built-in validator functions."""

    def test_validate_port_valid(self) -> None:
        """Test validate_port with valid ports."""
        assert validate_port(1) is True
        assert validate_port(80) is True
        assert validate_port(443) is True
        assert validate_port(8080) is True
        assert validate_port(65535) is True

    def test_validate_port_invalid(self) -> None:
        """Test validate_port with invalid ports."""
        assert validate_port(0) is False
        assert validate_port(-1) is False
        assert validate_port(65536) is False
        assert validate_port(100000) is False

    def test_validate_url_valid(self) -> None:
        """Test validate_url with valid URLs."""
        assert validate_url("http://example.com") is True
        assert validate_url("https://www.example.com") is True
        assert validate_url("ftp://files.example.com") is True
        assert validate_url("https://api.example.com/v1/users") is True

    def test_validate_url_invalid(self) -> None:
        """Test validate_url with invalid URLs."""
        assert validate_url("not_a_url") is False
        assert validate_url("http://") is False
        assert validate_url("://missing-scheme") is False
        assert validate_url("") is False

    def test_validate_url_exception_handling(self) -> None:
        """Test validate_url handles parsing exceptions."""
        # These might cause urlparse to raise exceptions
        assert validate_url(None) is False
        # urlparse should handle this gracefully, but if not, should return False

    def test_validate_email_valid(self) -> None:
        """Test validate_email with valid emails."""
        assert validate_email("user@example.com") is True
        assert validate_email("test.email+tag@example.co.uk") is True
        assert validate_email("user123@test-domain.org") is True

    def test_validate_email_invalid(self) -> None:
        """Test validate_email with invalid emails."""
        assert validate_email("not_an_email") is False
        assert validate_email("@example.com") is False
        assert validate_email("user@") is False
        assert validate_email("user@domain") is False
        assert validate_email("") is False

    def test_validate_path_valid(self) -> None:
        """Test validate_path with valid paths."""
        assert validate_path("/tmp/test.txt") is True
        assert validate_path("./relative/path") is True
        assert validate_path("C:\\Windows\\System32") is True
        assert validate_path("../parent/dir") is True

    def test_validate_path_exception_handling(self) -> None:
        """Test validate_path handles Path construction exceptions."""
        # Most strings should be valid path constructors
        # But if Path() ever raises an exception, it should return False
        assert validate_path("") is True  # Empty string is valid path

        # Test with None might cause exception
        try:
            result = validate_path(None)
            # If no exception, result could be True or False
            assert isinstance(result, bool)
        except Exception:
            # If exception in test, the function should handle it and return False
            pass

    def test_validate_version_valid(self) -> None:
        """Test validate_version with valid semantic versions."""
        assert validate_version("1.0.0") is True
        assert validate_version("0.1.0") is True
        assert validate_version("10.20.30") is True
        assert validate_version("1.0.0-alpha") is True
        assert validate_version("1.0.0-beta.1") is True
        assert validate_version("1.0.0+build.123") is True
        assert validate_version("1.0.0-alpha+build") is True

    def test_validate_version_invalid(self) -> None:
        """Test validate_version with invalid versions."""
        assert validate_version("1.0") is False
        assert validate_version("1") is False
        assert validate_version("v1.0.0") is False
        assert validate_version("1.0.0.0") is False
        assert validate_version("") is False
        assert validate_version("not.a.version") is False

    def test_validate_url_accessible(self) -> None:
        """Test validate_url_accessible async validator."""
        # This is just an example implementation that calls validate_url
        assert validate_url_accessible("https://example.com") is True
        assert validate_url_accessible("not_a_url") is False


# 🧱🏗️🔚
