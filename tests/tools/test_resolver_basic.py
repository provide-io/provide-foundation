#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Foundation tool version resolver."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.tools.resolver import VersionResolver


class TestVersionResolver(FoundationTestCase):
    """Test VersionResolver class."""

    def test_version_resolver_init(self) -> None:
        """Test VersionResolver initialization."""
        resolver = VersionResolver()
        assert resolver is not None

    def test_resolve_empty_available_list(self) -> None:
        """Test resolve returns None for empty available list."""
        resolver = VersionResolver()
        result = resolver.resolve("1.0.0", [])
        assert result is None

    def test_resolve_latest_stable(self) -> None:
        """Test resolving 'latest' to stable version."""
        resolver = VersionResolver()
        available = ["1.0.0", "1.1.0", "2.0.0", "2.1.0-beta", "1.5.0-alpha"]

        result = resolver.resolve("latest", available)
        assert result == "2.0.0"

    def test_resolve_latest_beta(self) -> None:
        """Test resolving 'latest-beta' to pre-release version."""
        resolver = VersionResolver()
        available = ["1.0.0", "1.1.0", "2.0.0", "2.1.0-beta", "1.5.0-alpha"]

        result = resolver.resolve("latest-beta", available)
        assert result == "2.1.0-beta"

    def test_resolve_latest_prerelease(self) -> None:
        """Test resolving 'latest-prerelease' alias."""
        resolver = VersionResolver()
        available = ["1.0.0", "2.1.0-beta", "1.5.0-alpha"]

        result = resolver.resolve("latest-prerelease", available)
        assert result == "2.1.0-beta"

    def test_resolve_latest_any(self) -> None:
        """Test resolving 'latest-any' to any version."""
        resolver = VersionResolver()
        available = ["1.0.0", "1.1.0", "2.0.0", "2.1.0-beta", "3.0.0-alpha"]

        result = resolver.resolve("latest-any", available)
        assert result == "3.0.0-alpha"

    def test_resolve_exact_match(self) -> None:
        """Test resolving exact version match."""
        resolver = VersionResolver()
        available = ["1.0.0", "1.1.0", "2.0.0"]

        result = resolver.resolve("1.1.0", available)
        assert result == "1.1.0"

    def test_resolve_exact_no_match(self) -> None:
        """Test resolving exact version with no match."""
        resolver = VersionResolver()
        available = ["1.0.0", "1.1.0", "2.0.0"]

        result = resolver.resolve("1.2.0", available)
        assert result is None

    def test_resolve_tilde_range(self) -> None:
        """Test resolving tilde range (~1.2.3)."""
        resolver = VersionResolver()
        available = ["1.2.0", "1.2.3", "1.2.5", "1.3.0", "2.0.0"]

        result = resolver.resolve("~1.2.3", available)
        assert result == "1.2.5"

    def test_resolve_tilde_range_no_patch(self) -> None:
        """Test resolving tilde range without patch version."""
        resolver = VersionResolver()
        available = ["1.2.0", "1.2.3", "1.2.5", "1.3.0", "2.0.0"]

        result = resolver.resolve("~1.2", available)
        assert result == "1.2.5"

    def test_resolve_caret_range(self) -> None:
        """Test resolving caret range (^1.2.3)."""
        resolver = VersionResolver()
        available = ["1.2.0", "1.2.3", "1.5.0", "2.0.0", "0.9.0"]

        result = resolver.resolve("^1.2.3", available)
        assert result == "1.5.0"

    def test_resolve_wildcard_patch(self) -> None:
        """Test resolving wildcard for patch version."""
        resolver = VersionResolver()
        available = ["1.2.0", "1.2.3", "1.2.5", "1.3.0", "2.0.0"]

        result = resolver.resolve("1.2.*", available)
        assert result == "1.2.5"

    def test_resolve_wildcard_minor(self) -> None:
        """Test resolving wildcard for minor version."""
        resolver = VersionResolver()
        available = ["1.0.0", "1.2.3", "1.5.0", "2.0.0"]

        result = resolver.resolve("1.*", available)
        assert result == "1.5.0"

    def test_resolve_wildcard_no_match(self) -> None:
        """Test resolving wildcard with no matches."""
        resolver = VersionResolver()
        available = ["1.0.0", "1.2.3", "2.0.0"]

        result = resolver.resolve("3.*", available)
        assert result is None

    def test_resolve_whitespace_trimming(self) -> None:
        """Test that whitespace in spec is trimmed."""
        resolver = VersionResolver()
        available = ["1.0.0", "2.0.0"]

        result = resolver.resolve("  latest  ", available)
        assert result == "2.0.0"


# 🧱🏗️🔚
