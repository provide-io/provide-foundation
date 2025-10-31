#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import re

from provide.foundation.errors import FoundationError
from provide.foundation.logger import get_logger

"""Version resolution for tool management.

Provides sophisticated version resolution including latest,
semver ranges, wildcards, and pre-release handling.
"""

log = get_logger(__name__)


class ResolutionError(FoundationError):
    """Raised when version resolution fails."""


class VersionResolver:
    """Resolve version specifications to concrete versions.

    Supports:
    - "latest": Most recent stable version
    - "latest-beta": Most recent pre-release
    - "~1.2.3": Patch version range
    - "^1.2.3": Minor version range
    - "1.2.*": Wildcard matching
    - Exact versions
    """

    def __init__(self) -> None:
        """Initialize version resolver with pattern cache."""
        self._pattern_cache: dict[str, re.Pattern[str]] = {}

    def resolve(self, spec: str, available: list[str]) -> str | None:
        """Resolve a version specification to a concrete version.

        Args:
            spec: Version specification.
            available: List of available versions.

        Returns:
            Resolved version string, or None if not found.

        """
        if not available:
            return None

        spec = spec.strip()

        # Handle special keywords
        if spec == "latest":
            return self.get_latest_stable(available)
        if spec == "latest-beta" or spec == "latest-prerelease":
            return self.get_latest_prerelease(available)
        if spec == "latest-any":
            return self.get_latest_any(available)

        # Handle ranges
        if spec.startswith("~"):
            return self.resolve_tilde(spec[1:], available)
        if spec.startswith("^"):
            return self.resolve_caret(spec[1:], available)

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def get_latest_stable(self, versions: list[str]) -> str | None:
        """Get latest stable version (no pre-release).

        Args:
            versions: List of available versions.

        Returns:
            Latest stable version, or None if no stable versions.

        """
        stable = [v for v in versions if not self.is_prerelease(v)]
        if not stable:
            return None

        return self.sort_versions(stable)[-1]

    def get_latest_prerelease(self, versions: list[str]) -> str | None:
        """Get latest pre-release version.

        Args:
            versions: List of available versions.

        Returns:
            Latest pre-release version, or None if no pre-releases.

        """
        prerelease = [v for v in versions if self.is_prerelease(v)]
        if not prerelease:
            return None

        return self.sort_versions(prerelease)[-1]

    def get_latest_any(self, versions: list[str]) -> str | None:
        """Get latest version (including pre-releases).

        Args:
            versions: List of available versions.

        Returns:
            Latest version, or None if list is empty.

        """
        if not versions:
            return None

        return self.sort_versions(versions)[-1]

    def is_prerelease(self, version: str) -> bool:
        """Check if version is a pre-release.

        Args:
            version: Version string.

        Returns:
            True if version appears to be pre-release.

        """
        # Common pre-release indicators
        prerelease_patterns = [
            r"-alpha",
            r"-beta",
            r"-rc",
            r"-dev",
            r"-preview",
            r"-pre",
            r"-snapshot",
            r"\.dev\d+",
            r"a\d+$",  # 1.0a1
            r"b\d+$",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def resolve_tilde(self, base: str, available: list[str]) -> str | None:
        """Resolve tilde range (~1.2.3 means >=1.2.3 <1.3.0).

        Args:
            base: Base version without tilde.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        try:
            parts = self.parse_version(base)
            if len(parts) < 2:
                return None

            major, minor = parts[0], parts[1]

            # Filter versions that match the constraint
            matches = []
            for v in available:
                v_parts = self.parse_version(v)
                if len(v_parts) >= 2 and v_parts[0] == major and v_parts[1] == minor:
                    if len(parts) >= 3:
                        # If patch specified, must be >= base patch
                        if len(v_parts) >= 3 and v_parts[2] >= parts[2]:
                            matches.append(v)
                    else:
                        matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve tilde range {base}: {e}")

        return None

    def resolve_caret(self, base: str, available: list[str]) -> str | None:
        """Resolve caret range (^1.2.3 means >=1.2.3 <2.0.0).

        Args:
            base: Base version without caret.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        try:
            parts = self.parse_version(base)
            if not parts:
                return None

            major = parts[0]

            # Filter versions that match the constraint
            matches = []
            for v in available:
                v_parts = self.parse_version(v)
                if v_parts and v_parts[0] == major and self.compare_versions(v, base) >= 0:
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def resolve_wildcard(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(".", r"\.")
        regex_pattern = regex_pattern.replace("*", r".*")
        regex_pattern = f"^{regex_pattern}$"

        try:
            # Check cache first
            if regex_pattern not in self._pattern_cache:
                self._pattern_cache[regex_pattern] = re.compile(regex_pattern)

            regex = self._pattern_cache[regex_pattern]
            matches = [v for v in available if regex.match(v)]

            if matches:
                # Return latest matching version
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve wildcard {pattern}: {e}")

        return None

    def parse_version(self, version: str) -> list[int]:
        """Parse version string into numeric components.

        Args:
            version: Version string.

        Returns:
            List of numeric version components.

        """
        # Extract just the numeric version part
        match = re.match(r"^v?(\d+(?:\.\d+)*)", version)
        if not match:
            return []

        version_str = match.group(1)
        parts = []

        for part in version_str.split("."):
            try:
                parts.append(int(part))
            except ValueError:
                break

        return parts

    def compare_versions(self, v1: str, v2: str) -> int:
        """Compare two versions.

        Args:
            v1: First version.
            v2: Second version.

        Returns:
            -1 if v1 < v2, 0 if equal, 1 if v1 > v2.

        """
        parts1 = self.parse_version(v1)
        parts2 = self.parse_version(v2)

        # Pad with zeros
        max_len = max(len(parts1), len(parts2))
        parts1.extend([0] * (max_len - len(parts1)))
        parts2.extend([0] * (max_len - len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def sort_versions(self, versions: list[str]) -> list[str]:
        """Sort versions in ascending order.

        Args:
            versions: List of version strings.

        Returns:
            Sorted list of versions.

        """
        return sorted(
            versions,
            key=lambda v: (
                self.parse_version(v),
                v,  # Secondary sort by string for pre-releases
            ),
        )


# 🧱🏗️🔚
