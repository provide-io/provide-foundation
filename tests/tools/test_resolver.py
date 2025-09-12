"""Tests for Foundation tool version resolver."""


from provide.foundation.tools.resolver import VersionResolver


class TestVersionResolver:
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
            "1.0.0", "1.0.1", "1.0.2",
            "1.1.0", "1.1.1", "1.2.0",
            "2.0.0", "2.0.1", "2.1.0",
            "3.0.0-alpha", "3.0.0-beta", "3.0.0"
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
            "v0.1.0", "v0.2.0", "v1.0.0",
            "v1.1.0", "v2.0.0", "v2.0.0-beta"
        ]

        # Should handle v prefixes
        assert resolver.resolve("latest", available) == "v2.0.0"
        assert resolver.resolve("^v1.0.0", available) == "v1.1.0"
        assert resolver.resolve("v1.*", available) == "v1.1.0"

    def test_python_style_version_resolution(self) -> None:
        """Test resolution with Python package style versions."""
        resolver = VersionResolver()
        available = [
            "1.0.0", "1.0.1", "1.1.0",
            "2.0.0a1", "2.0.0b1", "2.0.0rc1",
            "2.0.0", "2.0.0.dev1"
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
            for minor in range(0, 10):
                for patch in range(0, 10):
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
            "20.10.0", "20.10.1", "20.10.17",
            "24.0.0", "24.0.1", "24.0.2",
            "24.0.3-beta", "24.0.4-rc1"
        ]

        assert resolver.resolve("latest", available) == "24.0.2"
        assert resolver.resolve("~20.10.1", available) == "20.10.17"
        assert resolver.resolve("^24.0.0", available) == "24.0.4-rc1"  # Caret ranges include pre-releases
        assert resolver.resolve("latest-beta", available) == "24.0.4-rc1"

    def test_real_world_node_versions(self) -> None:
        """Test with real-world Node.js version patterns."""
        resolver = VersionResolver()
        available = [
            "16.14.0", "16.15.0", "16.16.0",
            "18.0.0", "18.1.0", "18.2.0",
            "19.0.0-pre", "19.0.0"
        ]

        assert resolver.resolve("latest", available) == "19.0.0"
        assert resolver.resolve("~16.15.0", available) == "16.15.0"  # Tilde only matches same minor version
        assert resolver.resolve("^18.0.0", available) == "18.2.0"
        assert resolver.resolve("18.*", available) == "18.2.0"
