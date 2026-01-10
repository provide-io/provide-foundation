#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Foundation tool version resolver helper methods."""

from __future__ import annotations

from provide.foundation.tools.resolver import VersionResolver


class TestVersionResolverHelpers:
    """Test VersionResolver helper methods."""

    def test_get_latest_stable_no_stable(self) -> None:
        """Test get_latest_stable with no stable versions."""
        resolver = VersionResolver()
        versions = ["1.0.0-alpha", "2.0.0-beta", "3.0.0-rc"]

        result = resolver.get_latest_stable(versions)
        assert result is None

    def test_get_latest_stable_mixed(self) -> None:
        """Test get_latest_stable with mixed versions."""
        resolver = VersionResolver()
        versions = ["1.0.0", "1.0.0-alpha", "2.0.0", "2.0.0-beta"]

        result = resolver.get_latest_stable(versions)
        assert result == "2.0.0"

    def test_get_latest_prerelease_no_prerelease(self) -> None:
        """Test get_latest_prerelease with no pre-releases."""
        resolver = VersionResolver()
        versions = ["1.0.0", "2.0.0", "3.0.0"]

        result = resolver.get_latest_prerelease(versions)
        assert result is None

    def test_get_latest_prerelease_mixed(self) -> None:
        """Test get_latest_prerelease with mixed versions."""
        resolver = VersionResolver()
        versions = ["1.0.0", "1.0.0-alpha", "2.0.0", "2.0.0-beta"]

        result = resolver.get_latest_prerelease(versions)
        assert result == "2.0.0-beta"

    def test_get_latest_any_empty(self) -> None:
        """Test get_latest_any with empty list."""
        resolver = VersionResolver()
        result = resolver.get_latest_any([])
        assert result is None

    def test_get_latest_any_single(self) -> None:
        """Test get_latest_any with single version."""
        resolver = VersionResolver()
        result = resolver.get_latest_any(["1.0.0"])
        assert result == "1.0.0"

    def test_is_prerelease_alpha(self) -> None:
        """Test is_prerelease with alpha versions."""
        resolver = VersionResolver()
        assert resolver.is_prerelease("1.0.0-alpha") is True
        assert resolver.is_prerelease("1.0.0-alpha.1") is True
        assert resolver.is_prerelease("1.0.0a1") is True

    def test_is_prerelease_beta(self) -> None:
        """Test is_prerelease with beta versions."""
        resolver = VersionResolver()
        assert resolver.is_prerelease("1.0.0-beta") is True
        assert resolver.is_prerelease("1.0.0-beta.2") is True
        assert resolver.is_prerelease("1.0.0b1") is True

    def test_is_prerelease_rc(self) -> None:
        """Test is_prerelease with release candidate versions."""
        resolver = VersionResolver()
        assert resolver.is_prerelease("1.0.0-rc") is True
        assert resolver.is_prerelease("1.0.0-rc.1") is True
        assert resolver.is_prerelease("1.0.0rc1") is True

    def test_is_prerelease_dev(self) -> None:
        """Test is_prerelease with dev versions."""
        resolver = VersionResolver()
        assert resolver.is_prerelease("1.0.0-dev") is True
        assert resolver.is_prerelease("1.0.0.dev1") is True

    def test_is_prerelease_other_patterns(self) -> None:
        """Test is_prerelease with other pre-release patterns."""
        resolver = VersionResolver()
        assert resolver.is_prerelease("1.0.0-preview") is True
        assert resolver.is_prerelease("1.0.0-pre") is True
        assert resolver.is_prerelease("1.0.0-snapshot") is True

    def test_is_prerelease_stable(self) -> None:
        """Test is_prerelease with stable versions."""
        resolver = VersionResolver()
        assert resolver.is_prerelease("1.0.0") is False
        assert resolver.is_prerelease("2.5.10") is False
        assert resolver.is_prerelease("v1.0.0") is False

    def test_parse_version_basic(self) -> None:
        """Test parse_version with basic versions."""
        resolver = VersionResolver()
        assert resolver.parse_version("1.2.3") == [1, 2, 3]
        assert resolver.parse_version("0.1.0") == [0, 1, 0]
        assert resolver.parse_version("10.20.30") == [10, 20, 30]

    def test_parse_version_with_prefix(self) -> None:
        """Test parse_version with v prefix."""
        resolver = VersionResolver()
        assert resolver.parse_version("v1.2.3") == [1, 2, 3]
        assert resolver.parse_version("v0.1.0") == [0, 1, 0]

    def test_parse_version_with_prerelease(self) -> None:
        """Test parse_version ignores pre-release parts."""
        resolver = VersionResolver()
        assert resolver.parse_version("1.2.3-alpha") == [1, 2, 3]
        assert resolver.parse_version("2.0.0-beta.1") == [2, 0, 0]

    def test_parse_version_partial(self) -> None:
        """Test parse_version with partial versions."""
        resolver = VersionResolver()
        assert resolver.parse_version("1.2") == [1, 2]
        assert resolver.parse_version("3") == [3]

    def test_parse_version_invalid(self) -> None:
        """Test parse_version with invalid versions."""
        resolver = VersionResolver()
        assert resolver.parse_version("invalid") == []
        assert resolver.parse_version("") == []
        assert resolver.parse_version("abc.def") == []

    def test_compare_versions_equal(self) -> None:
        """Test compare_versions with equal versions."""
        resolver = VersionResolver()
        assert resolver.compare_versions("1.2.3", "1.2.3") == 0
        assert resolver.compare_versions("1.0.0", "1.0.0") == 0

    def test_compare_versions_less_than(self) -> None:
        """Test compare_versions with less than."""
        resolver = VersionResolver()
        assert resolver.compare_versions("1.0.0", "2.0.0") == -1
        assert resolver.compare_versions("1.2.3", "1.2.4") == -1
        assert resolver.compare_versions("1.1.0", "1.2.0") == -1

    def test_compare_versions_greater_than(self) -> None:
        """Test compare_versions with greater than."""
        resolver = VersionResolver()
        assert resolver.compare_versions("2.0.0", "1.0.0") == 1
        assert resolver.compare_versions("1.2.4", "1.2.3") == 1
        assert resolver.compare_versions("1.2.0", "1.1.0") == 1

    def test_compare_versions_different_lengths(self) -> None:
        """Test compare_versions with different version lengths."""
        resolver = VersionResolver()
        assert resolver.compare_versions("1.0", "1.0.0") == 0
        assert resolver.compare_versions("1.0.0", "1.0") == 0
        assert resolver.compare_versions("1.0", "1.0.1") == -1
        assert resolver.compare_versions("1.0.1", "1.0") == 1

    def test_sort_versions_basic(self) -> None:
        """Test sort_versions with basic sorting."""
        resolver = VersionResolver()
        versions = ["2.0.0", "1.0.0", "1.5.0", "3.0.0"]

        result = resolver.sort_versions(versions)
        assert result == ["1.0.0", "1.5.0", "2.0.0", "3.0.0"]

    def test_sort_versions_with_prerelease(self) -> None:
        """Test sort_versions with pre-release versions."""
        resolver = VersionResolver()
        versions = ["1.0.0", "1.0.0-beta", "1.0.0-alpha", "2.0.0"]

        result = resolver.sort_versions(versions)
        # Versions should be sorted in ascending order: stable before pre-releases at string level
        assert result[0] == "1.0.0"  # Stable version
        assert result[1] == "1.0.0-alpha"  # Alpha comes before beta alphabetically
        assert result[2] == "1.0.0-beta"
        assert result[-1] == "2.0.0"

    def test_sort_versions_mixed_lengths(self) -> None:
        """Test sort_versions with different version lengths."""
        resolver = VersionResolver()
        versions = ["1.0", "1.0.0", "1.0.1", "2.0"]

        result = resolver.sort_versions(versions)
        assert result == ["1.0", "1.0.0", "1.0.1", "2.0"]


# 🧱🏗️🔚
