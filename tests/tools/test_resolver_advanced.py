#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Foundation tool version resolver edge cases and integration."""

from __future__ import annotations

from provide.foundation.tools.resolver import VersionResolver


class TestVersionResolverEdgeCases:
    """Test edge cases and error conditions."""

    def test_resolve_tilde_invalid_version(self) -> None:
        """Test tilde resolution with invalid base version."""
        resolver = VersionResolver()
        available = ["1.0.0", "2.0.0"]

        result = resolver.resolve("~invalid", available)
        assert result is None

    def test_resolve_tilde_insufficient_parts(self) -> None:
        """Test tilde resolution with insufficient version parts."""
        resolver = VersionResolver()
        available = ["1.0.0", "2.0.0"]

        result = resolver.resolve("~1", available)
        assert result is None

    def test_resolve_caret_invalid_version(self) -> None:
        """Test caret resolution with invalid base version."""
        resolver = VersionResolver()
        available = ["1.0.0", "2.0.0"]

        result = resolver.resolve("^invalid", available)
        assert result is None

    def test_resolve_wildcard_invalid_regex(self) -> None:
        """Test wildcard resolution with invalid regex pattern."""
        resolver = VersionResolver()
        available = ["1.0.0", "2.0.0"]

        # This should not crash, just return None
        result = resolver.resolve("[", available)
        assert result is None

    def test_resolve_tilde_with_available_invalid_versions(self) -> None:
        """Test tilde resolution where available versions are invalid."""
        resolver = VersionResolver()
        available = ["invalid", "also-invalid", "1.2.3"]

        result = resolver.resolve("~1.2.0", available)
        assert result == "1.2.3"

    def test_resolve_caret_with_mixed_valid_invalid(self) -> None:
        """Test caret resolution with mix of valid and invalid versions."""
        resolver = VersionResolver()
        available = ["invalid", "1.0.0", "1.5.0", "bad-version", "2.0.0"]

        result = resolver.resolve("^1.0.0", available)
        assert result == "1.5.0"

    def test_parse_version_with_build_metadata(self) -> None:
        """Test parsing versions with build metadata."""
        resolver = VersionResolver()
        assert resolver.parse_version("1.2.3+build.1") == [1, 2, 3]
        assert resolver.parse_version("1.0.0+20220101") == [1, 0, 0]

    def test_compare_versions_with_unparseable(self) -> None:
        """Test comparing versions where one is unparseable."""
        resolver = VersionResolver()
        # Should handle gracefully by treating unparseable as empty
        result = resolver.compare_versions("invalid", "1.0.0")
        assert result == -1  # Empty version parts compare as less

    def test_sort_versions_with_invalid_versions(self) -> None:
        """Test sorting with some invalid versions."""
        resolver = VersionResolver()
        versions = ["1.0.0", "invalid", "2.0.0", "also-bad"]

        result = resolver.sort_versions(versions)
        # Should not crash, and valid versions should be in order
        valid_versions = [v for v in result if resolver.parse_version(v)]
        assert valid_versions == ["1.0.0", "2.0.0"]


class TestVersionResolverIntegration:
    """Integration tests for VersionResolver."""

    def test_npm_style_version_resolution(self) -> None:
        """Test resolution similar to npm semantic versioning."""
        resolver = VersionResolver()
        available = [
            "1.0.0",
            "1.0.1",
            "1.0.2",
            "1.1.0",
            "1.1.1",
            "1.2.0",
            "2.0.0",
            "2.0.1",
            "2.1.0",
            "3.0.0-alpha",
            "3.0.0-beta",
            "3.0.0",
        ]

        # Tilde should get latest patch
        assert resolver.resolve("~1.0.1", available) == "1.0.2"
        assert resolver.resolve("~1.1.0", available) == "1.1.1"

        # Caret should get latest minor
        assert resolver.resolve("^1.0.0", available) == "1.2.0"
        assert resolver.resolve("^2.0.0", available) == "2.1.0"

        # Latest should get stable
        assert resolver.resolve("latest", available) == "3.0.0"

        # Latest beta should get pre-release
        assert resolver.resolve("latest-beta", available) == "3.0.0-beta"

    def test_golang_style_version_resolution(self) -> None:
        """Test resolution with go module style versions."""
        resolver = VersionResolver()
        available = [
            "v0.1.0",
            "v0.2.0",
            "v1.0.0",
            "v1.1.0",
            "v2.0.0",
            "v2.0.0-beta",
        ]

        # Should handle v prefixes
        assert resolver.resolve("latest", available) == "v2.0.0"
        assert resolver.resolve("^v1.0.0", available) == "v1.1.0"
        assert resolver.resolve("v1.*", available) == "v1.1.0"

    def test_python_style_version_resolution(self) -> None:
        """Test resolution with Python package style versions."""
        resolver = VersionResolver()
        available = [
            "1.0.0",
            "1.0.1",
            "1.1.0",
            "2.0.0a1",
            "2.0.0b1",
            "2.0.0rc1",
            "2.0.0",
            "2.0.0.dev1",
        ]

        # Should identify Python pre-releases
        assert resolver.is_prerelease("2.0.0a1") is True
        assert resolver.is_prerelease("2.0.0b1") is True
        assert resolver.is_prerelease("2.0.0rc1") is True
        assert resolver.is_prerelease("2.0.0.dev1") is True

        assert resolver.resolve("latest", available) == "2.0.0"
        assert resolver.resolve("latest-beta", available) in ["2.0.0rc1", "2.0.0.dev1"]

    def test_performance_with_large_version_list(self) -> None:
        """Test performance with many versions."""
        resolver = VersionResolver()

        # Generate lots of versions
        available = []
        for major in range(1, 6):
            for minor in range(10):
                for patch in range(10):
                    available.append(f"{major}.{minor}.{patch}")

        # Should still be fast
        result = resolver.resolve("latest", available)
        assert result == "5.9.9"

        result = resolver.resolve("^2.5.0", available)
        assert result == "2.9.9"

    def test_real_world_docker_versions(self) -> None:
        """Test with real-world Docker version patterns."""
        resolver = VersionResolver()
        available = [
            "20.10.0",
            "20.10.1",
            "20.10.17",
            "24.0.0",
            "24.0.1",
            "24.0.2",
            "24.0.3-beta",
            "24.0.4-rc1",
        ]

        assert resolver.resolve("latest", available) == "24.0.2"
        assert resolver.resolve("~20.10.1", available) == "20.10.17"
        assert resolver.resolve("^24.0.0", available) == "24.0.4-rc1"  # Caret ranges include pre-releases
        assert resolver.resolve("latest-beta", available) == "24.0.4-rc1"

    def test_real_world_node_versions(self) -> None:
        """Test with real-world Node.js version patterns."""
        resolver = VersionResolver()
        available = [
            "16.14.0",
            "16.15.0",
            "16.16.0",
            "18.0.0",
            "18.1.0",
            "18.2.0",
            "19.0.0-pre",
            "19.0.0",
        ]

        assert resolver.resolve("latest", available) == "19.0.0"
        assert resolver.resolve("~16.15.0", available) == "16.15.0"  # Tilde only matches same minor version
        assert resolver.resolve("^18.0.0", available) == "18.2.0"
        assert resolver.resolve("18.*", available) == "18.2.0"


# 🧱🏗️🔚
