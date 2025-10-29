# provide/foundation/tools/resolver.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re

from provide.foundation.errors import FoundationError
from provide.foundation.logger import get_logger

"""Version resolution for tool management.

Provides sophisticated version resolution including latest,
semver ranges, wildcards, and pre-release handling.
"""

log = get_logger(__name__)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    def xǁVersionResolverǁ__init____mutmut_orig(self) -> None:
        """Initialize version resolver with pattern cache."""
        self._pattern_cache: dict[str, re.Pattern[str]] = {}

    def xǁVersionResolverǁ__init____mutmut_1(self) -> None:
        """Initialize version resolver with pattern cache."""
        self._pattern_cache: dict[str, re.Pattern[str]] = None

    xǁVersionResolverǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁVersionResolverǁ__init____mutmut_1": xǁVersionResolverǁ__init____mutmut_1
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁVersionResolverǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁVersionResolverǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁVersionResolverǁ__init____mutmut_orig)
    xǁVersionResolverǁ__init____mutmut_orig.__name__ = "xǁVersionResolverǁ__init__"

    def xǁVersionResolverǁresolve__mutmut_orig(self, spec: str, available: list[str]) -> str | None:
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

    def xǁVersionResolverǁresolve__mutmut_1(self, spec: str, available: list[str]) -> str | None:
        """Resolve a version specification to a concrete version.

        Args:
            spec: Version specification.
            available: List of available versions.

        Returns:
            Resolved version string, or None if not found.

        """
        if available:
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

    def xǁVersionResolverǁresolve__mutmut_2(self, spec: str, available: list[str]) -> str | None:
        """Resolve a version specification to a concrete version.

        Args:
            spec: Version specification.
            available: List of available versions.

        Returns:
            Resolved version string, or None if not found.

        """
        if not available:
            return None

        spec = None

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

    def xǁVersionResolverǁresolve__mutmut_3(self, spec: str, available: list[str]) -> str | None:
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
        if spec != "latest":
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

    def xǁVersionResolverǁresolve__mutmut_4(self, spec: str, available: list[str]) -> str | None:
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
        if spec == "XXlatestXX":
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

    def xǁVersionResolverǁresolve__mutmut_5(self, spec: str, available: list[str]) -> str | None:
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
        if spec == "LATEST":
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

    def xǁVersionResolverǁresolve__mutmut_6(self, spec: str, available: list[str]) -> str | None:
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
            return self.get_latest_stable(None)
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

    def xǁVersionResolverǁresolve__mutmut_7(self, spec: str, available: list[str]) -> str | None:
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
        if spec == "latest-beta" and spec == "latest-prerelease":
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

    def xǁVersionResolverǁresolve__mutmut_8(self, spec: str, available: list[str]) -> str | None:
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
        if spec != "latest-beta" or spec == "latest-prerelease":
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

    def xǁVersionResolverǁresolve__mutmut_9(self, spec: str, available: list[str]) -> str | None:
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
        if spec == "XXlatest-betaXX" or spec == "latest-prerelease":
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

    def xǁVersionResolverǁresolve__mutmut_10(self, spec: str, available: list[str]) -> str | None:
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
        if spec == "LATEST-BETA" or spec == "latest-prerelease":
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

    def xǁVersionResolverǁresolve__mutmut_11(self, spec: str, available: list[str]) -> str | None:
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
        if spec == "latest-beta" or spec != "latest-prerelease":
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

    def xǁVersionResolverǁresolve__mutmut_12(self, spec: str, available: list[str]) -> str | None:
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
        if spec == "latest-beta" or spec == "XXlatest-prereleaseXX":
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

    def xǁVersionResolverǁresolve__mutmut_13(self, spec: str, available: list[str]) -> str | None:
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
        if spec == "latest-beta" or spec == "LATEST-PRERELEASE":
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

    def xǁVersionResolverǁresolve__mutmut_14(self, spec: str, available: list[str]) -> str | None:
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
            return self.get_latest_prerelease(None)
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

    def xǁVersionResolverǁresolve__mutmut_15(self, spec: str, available: list[str]) -> str | None:
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
        if spec != "latest-any":
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

    def xǁVersionResolverǁresolve__mutmut_16(self, spec: str, available: list[str]) -> str | None:
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
        if spec == "XXlatest-anyXX":
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

    def xǁVersionResolverǁresolve__mutmut_17(self, spec: str, available: list[str]) -> str | None:
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
        if spec == "LATEST-ANY":
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

    def xǁVersionResolverǁresolve__mutmut_18(self, spec: str, available: list[str]) -> str | None:
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
            return self.get_latest_any(None)

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

    def xǁVersionResolverǁresolve__mutmut_19(self, spec: str, available: list[str]) -> str | None:
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
        if spec.startswith(None):
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

    def xǁVersionResolverǁresolve__mutmut_20(self, spec: str, available: list[str]) -> str | None:
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
        if spec.startswith("XX~XX"):
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

    def xǁVersionResolverǁresolve__mutmut_21(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_tilde(None, available)
        if spec.startswith("^"):
            return self.resolve_caret(spec[1:], available)

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_22(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_tilde(spec[1:], None)
        if spec.startswith("^"):
            return self.resolve_caret(spec[1:], available)

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_23(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_tilde(available)
        if spec.startswith("^"):
            return self.resolve_caret(spec[1:], available)

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_24(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_tilde(
                spec[1:],
            )
        if spec.startswith("^"):
            return self.resolve_caret(spec[1:], available)

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_25(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_tilde(spec[2:], available)
        if spec.startswith("^"):
            return self.resolve_caret(spec[1:], available)

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_26(self, spec: str, available: list[str]) -> str | None:
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
        if spec.startswith(None):
            return self.resolve_caret(spec[1:], available)

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_27(self, spec: str, available: list[str]) -> str | None:
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
        if spec.startswith("XX^XX"):
            return self.resolve_caret(spec[1:], available)

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_28(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_caret(None, available)

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_29(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_caret(spec[1:], None)

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_30(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_caret(available)

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_31(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_caret(
                spec[1:],
            )

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_32(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_caret(spec[2:], available)

        # Handle wildcards
        if "*" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_33(self, spec: str, available: list[str]) -> str | None:
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
        if "XX*XX" in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_34(self, spec: str, available: list[str]) -> str | None:
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
        if "*" not in spec:
            return self.resolve_wildcard(spec, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_35(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_wildcard(None, available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_36(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_wildcard(spec, None)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_37(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_wildcard(available)

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_38(self, spec: str, available: list[str]) -> str | None:
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
            return self.resolve_wildcard(
                spec,
            )

        # Exact match
        if spec in available:
            return spec

        return None

    def xǁVersionResolverǁresolve__mutmut_39(self, spec: str, available: list[str]) -> str | None:
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
        if spec not in available:
            return spec

        return None

    xǁVersionResolverǁresolve__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁVersionResolverǁresolve__mutmut_1": xǁVersionResolverǁresolve__mutmut_1,
        "xǁVersionResolverǁresolve__mutmut_2": xǁVersionResolverǁresolve__mutmut_2,
        "xǁVersionResolverǁresolve__mutmut_3": xǁVersionResolverǁresolve__mutmut_3,
        "xǁVersionResolverǁresolve__mutmut_4": xǁVersionResolverǁresolve__mutmut_4,
        "xǁVersionResolverǁresolve__mutmut_5": xǁVersionResolverǁresolve__mutmut_5,
        "xǁVersionResolverǁresolve__mutmut_6": xǁVersionResolverǁresolve__mutmut_6,
        "xǁVersionResolverǁresolve__mutmut_7": xǁVersionResolverǁresolve__mutmut_7,
        "xǁVersionResolverǁresolve__mutmut_8": xǁVersionResolverǁresolve__mutmut_8,
        "xǁVersionResolverǁresolve__mutmut_9": xǁVersionResolverǁresolve__mutmut_9,
        "xǁVersionResolverǁresolve__mutmut_10": xǁVersionResolverǁresolve__mutmut_10,
        "xǁVersionResolverǁresolve__mutmut_11": xǁVersionResolverǁresolve__mutmut_11,
        "xǁVersionResolverǁresolve__mutmut_12": xǁVersionResolverǁresolve__mutmut_12,
        "xǁVersionResolverǁresolve__mutmut_13": xǁVersionResolverǁresolve__mutmut_13,
        "xǁVersionResolverǁresolve__mutmut_14": xǁVersionResolverǁresolve__mutmut_14,
        "xǁVersionResolverǁresolve__mutmut_15": xǁVersionResolverǁresolve__mutmut_15,
        "xǁVersionResolverǁresolve__mutmut_16": xǁVersionResolverǁresolve__mutmut_16,
        "xǁVersionResolverǁresolve__mutmut_17": xǁVersionResolverǁresolve__mutmut_17,
        "xǁVersionResolverǁresolve__mutmut_18": xǁVersionResolverǁresolve__mutmut_18,
        "xǁVersionResolverǁresolve__mutmut_19": xǁVersionResolverǁresolve__mutmut_19,
        "xǁVersionResolverǁresolve__mutmut_20": xǁVersionResolverǁresolve__mutmut_20,
        "xǁVersionResolverǁresolve__mutmut_21": xǁVersionResolverǁresolve__mutmut_21,
        "xǁVersionResolverǁresolve__mutmut_22": xǁVersionResolverǁresolve__mutmut_22,
        "xǁVersionResolverǁresolve__mutmut_23": xǁVersionResolverǁresolve__mutmut_23,
        "xǁVersionResolverǁresolve__mutmut_24": xǁVersionResolverǁresolve__mutmut_24,
        "xǁVersionResolverǁresolve__mutmut_25": xǁVersionResolverǁresolve__mutmut_25,
        "xǁVersionResolverǁresolve__mutmut_26": xǁVersionResolverǁresolve__mutmut_26,
        "xǁVersionResolverǁresolve__mutmut_27": xǁVersionResolverǁresolve__mutmut_27,
        "xǁVersionResolverǁresolve__mutmut_28": xǁVersionResolverǁresolve__mutmut_28,
        "xǁVersionResolverǁresolve__mutmut_29": xǁVersionResolverǁresolve__mutmut_29,
        "xǁVersionResolverǁresolve__mutmut_30": xǁVersionResolverǁresolve__mutmut_30,
        "xǁVersionResolverǁresolve__mutmut_31": xǁVersionResolverǁresolve__mutmut_31,
        "xǁVersionResolverǁresolve__mutmut_32": xǁVersionResolverǁresolve__mutmut_32,
        "xǁVersionResolverǁresolve__mutmut_33": xǁVersionResolverǁresolve__mutmut_33,
        "xǁVersionResolverǁresolve__mutmut_34": xǁVersionResolverǁresolve__mutmut_34,
        "xǁVersionResolverǁresolve__mutmut_35": xǁVersionResolverǁresolve__mutmut_35,
        "xǁVersionResolverǁresolve__mutmut_36": xǁVersionResolverǁresolve__mutmut_36,
        "xǁVersionResolverǁresolve__mutmut_37": xǁVersionResolverǁresolve__mutmut_37,
        "xǁVersionResolverǁresolve__mutmut_38": xǁVersionResolverǁresolve__mutmut_38,
        "xǁVersionResolverǁresolve__mutmut_39": xǁVersionResolverǁresolve__mutmut_39,
    }

    def resolve(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁVersionResolverǁresolve__mutmut_orig"),
            object.__getattribute__(self, "xǁVersionResolverǁresolve__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    resolve.__signature__ = _mutmut_signature(xǁVersionResolverǁresolve__mutmut_orig)
    xǁVersionResolverǁresolve__mutmut_orig.__name__ = "xǁVersionResolverǁresolve"

    def xǁVersionResolverǁget_latest_stable__mutmut_orig(self, versions: list[str]) -> str | None:
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

    def xǁVersionResolverǁget_latest_stable__mutmut_1(self, versions: list[str]) -> str | None:
        """Get latest stable version (no pre-release).

        Args:
            versions: List of available versions.

        Returns:
            Latest stable version, or None if no stable versions.

        """
        stable = None
        if not stable:
            return None

        return self.sort_versions(stable)[-1]

    def xǁVersionResolverǁget_latest_stable__mutmut_2(self, versions: list[str]) -> str | None:
        """Get latest stable version (no pre-release).

        Args:
            versions: List of available versions.

        Returns:
            Latest stable version, or None if no stable versions.

        """
        stable = [v for v in versions if self.is_prerelease(v)]
        if not stable:
            return None

        return self.sort_versions(stable)[-1]

    def xǁVersionResolverǁget_latest_stable__mutmut_3(self, versions: list[str]) -> str | None:
        """Get latest stable version (no pre-release).

        Args:
            versions: List of available versions.

        Returns:
            Latest stable version, or None if no stable versions.

        """
        stable = [v for v in versions if not self.is_prerelease(None)]
        if not stable:
            return None

        return self.sort_versions(stable)[-1]

    def xǁVersionResolverǁget_latest_stable__mutmut_4(self, versions: list[str]) -> str | None:
        """Get latest stable version (no pre-release).

        Args:
            versions: List of available versions.

        Returns:
            Latest stable version, or None if no stable versions.

        """
        stable = [v for v in versions if not self.is_prerelease(v)]
        if stable:
            return None

        return self.sort_versions(stable)[-1]

    def xǁVersionResolverǁget_latest_stable__mutmut_5(self, versions: list[str]) -> str | None:
        """Get latest stable version (no pre-release).

        Args:
            versions: List of available versions.

        Returns:
            Latest stable version, or None if no stable versions.

        """
        stable = [v for v in versions if not self.is_prerelease(v)]
        if not stable:
            return None

        return self.sort_versions(None)[-1]

    def xǁVersionResolverǁget_latest_stable__mutmut_6(self, versions: list[str]) -> str | None:
        """Get latest stable version (no pre-release).

        Args:
            versions: List of available versions.

        Returns:
            Latest stable version, or None if no stable versions.

        """
        stable = [v for v in versions if not self.is_prerelease(v)]
        if not stable:
            return None

        return self.sort_versions(stable)[+1]

    def xǁVersionResolverǁget_latest_stable__mutmut_7(self, versions: list[str]) -> str | None:
        """Get latest stable version (no pre-release).

        Args:
            versions: List of available versions.

        Returns:
            Latest stable version, or None if no stable versions.

        """
        stable = [v for v in versions if not self.is_prerelease(v)]
        if not stable:
            return None

        return self.sort_versions(stable)[-2]

    xǁVersionResolverǁget_latest_stable__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁVersionResolverǁget_latest_stable__mutmut_1": xǁVersionResolverǁget_latest_stable__mutmut_1,
        "xǁVersionResolverǁget_latest_stable__mutmut_2": xǁVersionResolverǁget_latest_stable__mutmut_2,
        "xǁVersionResolverǁget_latest_stable__mutmut_3": xǁVersionResolverǁget_latest_stable__mutmut_3,
        "xǁVersionResolverǁget_latest_stable__mutmut_4": xǁVersionResolverǁget_latest_stable__mutmut_4,
        "xǁVersionResolverǁget_latest_stable__mutmut_5": xǁVersionResolverǁget_latest_stable__mutmut_5,
        "xǁVersionResolverǁget_latest_stable__mutmut_6": xǁVersionResolverǁget_latest_stable__mutmut_6,
        "xǁVersionResolverǁget_latest_stable__mutmut_7": xǁVersionResolverǁget_latest_stable__mutmut_7,
    }

    def get_latest_stable(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁVersionResolverǁget_latest_stable__mutmut_orig"),
            object.__getattribute__(self, "xǁVersionResolverǁget_latest_stable__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_latest_stable.__signature__ = _mutmut_signature(xǁVersionResolverǁget_latest_stable__mutmut_orig)
    xǁVersionResolverǁget_latest_stable__mutmut_orig.__name__ = "xǁVersionResolverǁget_latest_stable"

    def xǁVersionResolverǁget_latest_prerelease__mutmut_orig(self, versions: list[str]) -> str | None:
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

    def xǁVersionResolverǁget_latest_prerelease__mutmut_1(self, versions: list[str]) -> str | None:
        """Get latest pre-release version.

        Args:
            versions: List of available versions.

        Returns:
            Latest pre-release version, or None if no pre-releases.

        """
        prerelease = None
        if not prerelease:
            return None

        return self.sort_versions(prerelease)[-1]

    def xǁVersionResolverǁget_latest_prerelease__mutmut_2(self, versions: list[str]) -> str | None:
        """Get latest pre-release version.

        Args:
            versions: List of available versions.

        Returns:
            Latest pre-release version, or None if no pre-releases.

        """
        prerelease = [v for v in versions if self.is_prerelease(None)]
        if not prerelease:
            return None

        return self.sort_versions(prerelease)[-1]

    def xǁVersionResolverǁget_latest_prerelease__mutmut_3(self, versions: list[str]) -> str | None:
        """Get latest pre-release version.

        Args:
            versions: List of available versions.

        Returns:
            Latest pre-release version, or None if no pre-releases.

        """
        prerelease = [v for v in versions if self.is_prerelease(v)]
        if prerelease:
            return None

        return self.sort_versions(prerelease)[-1]

    def xǁVersionResolverǁget_latest_prerelease__mutmut_4(self, versions: list[str]) -> str | None:
        """Get latest pre-release version.

        Args:
            versions: List of available versions.

        Returns:
            Latest pre-release version, or None if no pre-releases.

        """
        prerelease = [v for v in versions if self.is_prerelease(v)]
        if not prerelease:
            return None

        return self.sort_versions(None)[-1]

    def xǁVersionResolverǁget_latest_prerelease__mutmut_5(self, versions: list[str]) -> str | None:
        """Get latest pre-release version.

        Args:
            versions: List of available versions.

        Returns:
            Latest pre-release version, or None if no pre-releases.

        """
        prerelease = [v for v in versions if self.is_prerelease(v)]
        if not prerelease:
            return None

        return self.sort_versions(prerelease)[+1]

    def xǁVersionResolverǁget_latest_prerelease__mutmut_6(self, versions: list[str]) -> str | None:
        """Get latest pre-release version.

        Args:
            versions: List of available versions.

        Returns:
            Latest pre-release version, or None if no pre-releases.

        """
        prerelease = [v for v in versions if self.is_prerelease(v)]
        if not prerelease:
            return None

        return self.sort_versions(prerelease)[-2]

    xǁVersionResolverǁget_latest_prerelease__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁVersionResolverǁget_latest_prerelease__mutmut_1": xǁVersionResolverǁget_latest_prerelease__mutmut_1,
        "xǁVersionResolverǁget_latest_prerelease__mutmut_2": xǁVersionResolverǁget_latest_prerelease__mutmut_2,
        "xǁVersionResolverǁget_latest_prerelease__mutmut_3": xǁVersionResolverǁget_latest_prerelease__mutmut_3,
        "xǁVersionResolverǁget_latest_prerelease__mutmut_4": xǁVersionResolverǁget_latest_prerelease__mutmut_4,
        "xǁVersionResolverǁget_latest_prerelease__mutmut_5": xǁVersionResolverǁget_latest_prerelease__mutmut_5,
        "xǁVersionResolverǁget_latest_prerelease__mutmut_6": xǁVersionResolverǁget_latest_prerelease__mutmut_6,
    }

    def get_latest_prerelease(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁVersionResolverǁget_latest_prerelease__mutmut_orig"),
            object.__getattribute__(self, "xǁVersionResolverǁget_latest_prerelease__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_latest_prerelease.__signature__ = _mutmut_signature(
        xǁVersionResolverǁget_latest_prerelease__mutmut_orig
    )
    xǁVersionResolverǁget_latest_prerelease__mutmut_orig.__name__ = "xǁVersionResolverǁget_latest_prerelease"

    def xǁVersionResolverǁget_latest_any__mutmut_orig(self, versions: list[str]) -> str | None:
        """Get latest version (including pre-releases).

        Args:
            versions: List of available versions.

        Returns:
            Latest version, or None if list is empty.

        """
        if not versions:
            return None

        return self.sort_versions(versions)[-1]

    def xǁVersionResolverǁget_latest_any__mutmut_1(self, versions: list[str]) -> str | None:
        """Get latest version (including pre-releases).

        Args:
            versions: List of available versions.

        Returns:
            Latest version, or None if list is empty.

        """
        if versions:
            return None

        return self.sort_versions(versions)[-1]

    def xǁVersionResolverǁget_latest_any__mutmut_2(self, versions: list[str]) -> str | None:
        """Get latest version (including pre-releases).

        Args:
            versions: List of available versions.

        Returns:
            Latest version, or None if list is empty.

        """
        if not versions:
            return None

        return self.sort_versions(None)[-1]

    def xǁVersionResolverǁget_latest_any__mutmut_3(self, versions: list[str]) -> str | None:
        """Get latest version (including pre-releases).

        Args:
            versions: List of available versions.

        Returns:
            Latest version, or None if list is empty.

        """
        if not versions:
            return None

        return self.sort_versions(versions)[+1]

    def xǁVersionResolverǁget_latest_any__mutmut_4(self, versions: list[str]) -> str | None:
        """Get latest version (including pre-releases).

        Args:
            versions: List of available versions.

        Returns:
            Latest version, or None if list is empty.

        """
        if not versions:
            return None

        return self.sort_versions(versions)[-2]

    xǁVersionResolverǁget_latest_any__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁVersionResolverǁget_latest_any__mutmut_1": xǁVersionResolverǁget_latest_any__mutmut_1,
        "xǁVersionResolverǁget_latest_any__mutmut_2": xǁVersionResolverǁget_latest_any__mutmut_2,
        "xǁVersionResolverǁget_latest_any__mutmut_3": xǁVersionResolverǁget_latest_any__mutmut_3,
        "xǁVersionResolverǁget_latest_any__mutmut_4": xǁVersionResolverǁget_latest_any__mutmut_4,
    }

    def get_latest_any(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁVersionResolverǁget_latest_any__mutmut_orig"),
            object.__getattribute__(self, "xǁVersionResolverǁget_latest_any__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_latest_any.__signature__ = _mutmut_signature(xǁVersionResolverǁget_latest_any__mutmut_orig)
    xǁVersionResolverǁget_latest_any__mutmut_orig.__name__ = "xǁVersionResolverǁget_latest_any"

    def xǁVersionResolverǁis_prerelease__mutmut_orig(self, version: str) -> bool:
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

    def xǁVersionResolverǁis_prerelease__mutmut_1(self, version: str) -> bool:
        """Check if version is a pre-release.

        Args:
            version: Version string.

        Returns:
            True if version appears to be pre-release.

        """
        # Common pre-release indicators
        prerelease_patterns = None

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_2(self, version: str) -> bool:
        """Check if version is a pre-release.

        Args:
            version: Version string.

        Returns:
            True if version appears to be pre-release.

        """
        # Common pre-release indicators
        prerelease_patterns = [
            r"XX-alphaXX",
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

    def xǁVersionResolverǁis_prerelease__mutmut_3(self, version: str) -> bool:
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

    def xǁVersionResolverǁis_prerelease__mutmut_4(self, version: str) -> bool:
        """Check if version is a pre-release.

        Args:
            version: Version string.

        Returns:
            True if version appears to be pre-release.

        """
        # Common pre-release indicators
        prerelease_patterns = [
            r"-ALPHA",
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

    def xǁVersionResolverǁis_prerelease__mutmut_5(self, version: str) -> bool:
        """Check if version is a pre-release.

        Args:
            version: Version string.

        Returns:
            True if version appears to be pre-release.

        """
        # Common pre-release indicators
        prerelease_patterns = [
            r"-alpha",
            r"XX-betaXX",
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

    def xǁVersionResolverǁis_prerelease__mutmut_6(self, version: str) -> bool:
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

    def xǁVersionResolverǁis_prerelease__mutmut_7(self, version: str) -> bool:
        """Check if version is a pre-release.

        Args:
            version: Version string.

        Returns:
            True if version appears to be pre-release.

        """
        # Common pre-release indicators
        prerelease_patterns = [
            r"-alpha",
            r"-BETA",
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

    def xǁVersionResolverǁis_prerelease__mutmut_8(self, version: str) -> bool:
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
            r"XX-rcXX",
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

    def xǁVersionResolverǁis_prerelease__mutmut_9(self, version: str) -> bool:
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

    def xǁVersionResolverǁis_prerelease__mutmut_10(self, version: str) -> bool:
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
            r"-RC",
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

    def xǁVersionResolverǁis_prerelease__mutmut_11(self, version: str) -> bool:
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
            r"XX-devXX",
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

    def xǁVersionResolverǁis_prerelease__mutmut_12(self, version: str) -> bool:
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

    def xǁVersionResolverǁis_prerelease__mutmut_13(self, version: str) -> bool:
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
            r"-DEV",
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

    def xǁVersionResolverǁis_prerelease__mutmut_14(self, version: str) -> bool:
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
            r"XX-previewXX",
            r"-pre",
            r"-snapshot",
            r"\.dev\d+",
            r"a\d+$",  # 1.0a1
            r"b\d+$",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_15(self, version: str) -> bool:
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

    def xǁVersionResolverǁis_prerelease__mutmut_16(self, version: str) -> bool:
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
            r"-PREVIEW",
            r"-pre",
            r"-snapshot",
            r"\.dev\d+",
            r"a\d+$",  # 1.0a1
            r"b\d+$",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_17(self, version: str) -> bool:
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
            r"XX-preXX",
            r"-snapshot",
            r"\.dev\d+",
            r"a\d+$",  # 1.0a1
            r"b\d+$",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_18(self, version: str) -> bool:
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

    def xǁVersionResolverǁis_prerelease__mutmut_19(self, version: str) -> bool:
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
            r"-PRE",
            r"-snapshot",
            r"\.dev\d+",
            r"a\d+$",  # 1.0a1
            r"b\d+$",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_20(self, version: str) -> bool:
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
            r"XX-snapshotXX",
            r"\.dev\d+",
            r"a\d+$",  # 1.0a1
            r"b\d+$",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_21(self, version: str) -> bool:
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

    def xǁVersionResolverǁis_prerelease__mutmut_22(self, version: str) -> bool:
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
            r"-SNAPSHOT",
            r"\.dev\d+",
            r"a\d+$",  # 1.0a1
            r"b\d+$",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_23(self, version: str) -> bool:
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
            r"XX\.dev\d+XX",
            r"a\d+$",  # 1.0a1
            r"b\d+$",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_24(self, version: str) -> bool:
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

    def xǁVersionResolverǁis_prerelease__mutmut_25(self, version: str) -> bool:
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
            r"\.DEV\d+",
            r"a\d+$",  # 1.0a1
            r"b\d+$",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_26(self, version: str) -> bool:
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
            r"XXa\d+$XX",  # 1.0a1
            r"b\d+$",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_27(self, version: str) -> bool:
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

    def xǁVersionResolverǁis_prerelease__mutmut_28(self, version: str) -> bool:
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
            r"A\d+$",  # 1.0a1
            r"b\d+$",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_29(self, version: str) -> bool:
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
            r"XXb\d+$XX",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_30(self, version: str) -> bool:
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

    def xǁVersionResolverǁis_prerelease__mutmut_31(self, version: str) -> bool:
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
            r"B\d+$",  # 1.0b2
            r"rc\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_32(self, version: str) -> bool:
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
            r"XXrc\d+$XX",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_33(self, version: str) -> bool:
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

    def xǁVersionResolverǁis_prerelease__mutmut_34(self, version: str) -> bool:
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
            r"RC\d+$",  # 1.0rc3
        ]

        version_lower = version.lower()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_35(self, version: str) -> bool:
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

        version_lower = None
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_36(self, version: str) -> bool:
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

        version_lower = version.upper()
        return any(re.search(pattern, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_37(self, version: str) -> bool:
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
        return any(None)

    def xǁVersionResolverǁis_prerelease__mutmut_38(self, version: str) -> bool:
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
        return any(re.search(None, version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_39(self, version: str) -> bool:
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
        return any(re.search(pattern, None) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_40(self, version: str) -> bool:
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
        return any(re.search(version_lower) for pattern in prerelease_patterns)

    def xǁVersionResolverǁis_prerelease__mutmut_41(self, version: str) -> bool:
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
        return any(
            re.search(
                pattern,
            )
            for pattern in prerelease_patterns
        )

    xǁVersionResolverǁis_prerelease__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁVersionResolverǁis_prerelease__mutmut_1": xǁVersionResolverǁis_prerelease__mutmut_1,
        "xǁVersionResolverǁis_prerelease__mutmut_2": xǁVersionResolverǁis_prerelease__mutmut_2,
        "xǁVersionResolverǁis_prerelease__mutmut_3": xǁVersionResolverǁis_prerelease__mutmut_3,
        "xǁVersionResolverǁis_prerelease__mutmut_4": xǁVersionResolverǁis_prerelease__mutmut_4,
        "xǁVersionResolverǁis_prerelease__mutmut_5": xǁVersionResolverǁis_prerelease__mutmut_5,
        "xǁVersionResolverǁis_prerelease__mutmut_6": xǁVersionResolverǁis_prerelease__mutmut_6,
        "xǁVersionResolverǁis_prerelease__mutmut_7": xǁVersionResolverǁis_prerelease__mutmut_7,
        "xǁVersionResolverǁis_prerelease__mutmut_8": xǁVersionResolverǁis_prerelease__mutmut_8,
        "xǁVersionResolverǁis_prerelease__mutmut_9": xǁVersionResolverǁis_prerelease__mutmut_9,
        "xǁVersionResolverǁis_prerelease__mutmut_10": xǁVersionResolverǁis_prerelease__mutmut_10,
        "xǁVersionResolverǁis_prerelease__mutmut_11": xǁVersionResolverǁis_prerelease__mutmut_11,
        "xǁVersionResolverǁis_prerelease__mutmut_12": xǁVersionResolverǁis_prerelease__mutmut_12,
        "xǁVersionResolverǁis_prerelease__mutmut_13": xǁVersionResolverǁis_prerelease__mutmut_13,
        "xǁVersionResolverǁis_prerelease__mutmut_14": xǁVersionResolverǁis_prerelease__mutmut_14,
        "xǁVersionResolverǁis_prerelease__mutmut_15": xǁVersionResolverǁis_prerelease__mutmut_15,
        "xǁVersionResolverǁis_prerelease__mutmut_16": xǁVersionResolverǁis_prerelease__mutmut_16,
        "xǁVersionResolverǁis_prerelease__mutmut_17": xǁVersionResolverǁis_prerelease__mutmut_17,
        "xǁVersionResolverǁis_prerelease__mutmut_18": xǁVersionResolverǁis_prerelease__mutmut_18,
        "xǁVersionResolverǁis_prerelease__mutmut_19": xǁVersionResolverǁis_prerelease__mutmut_19,
        "xǁVersionResolverǁis_prerelease__mutmut_20": xǁVersionResolverǁis_prerelease__mutmut_20,
        "xǁVersionResolverǁis_prerelease__mutmut_21": xǁVersionResolverǁis_prerelease__mutmut_21,
        "xǁVersionResolverǁis_prerelease__mutmut_22": xǁVersionResolverǁis_prerelease__mutmut_22,
        "xǁVersionResolverǁis_prerelease__mutmut_23": xǁVersionResolverǁis_prerelease__mutmut_23,
        "xǁVersionResolverǁis_prerelease__mutmut_24": xǁVersionResolverǁis_prerelease__mutmut_24,
        "xǁVersionResolverǁis_prerelease__mutmut_25": xǁVersionResolverǁis_prerelease__mutmut_25,
        "xǁVersionResolverǁis_prerelease__mutmut_26": xǁVersionResolverǁis_prerelease__mutmut_26,
        "xǁVersionResolverǁis_prerelease__mutmut_27": xǁVersionResolverǁis_prerelease__mutmut_27,
        "xǁVersionResolverǁis_prerelease__mutmut_28": xǁVersionResolverǁis_prerelease__mutmut_28,
        "xǁVersionResolverǁis_prerelease__mutmut_29": xǁVersionResolverǁis_prerelease__mutmut_29,
        "xǁVersionResolverǁis_prerelease__mutmut_30": xǁVersionResolverǁis_prerelease__mutmut_30,
        "xǁVersionResolverǁis_prerelease__mutmut_31": xǁVersionResolverǁis_prerelease__mutmut_31,
        "xǁVersionResolverǁis_prerelease__mutmut_32": xǁVersionResolverǁis_prerelease__mutmut_32,
        "xǁVersionResolverǁis_prerelease__mutmut_33": xǁVersionResolverǁis_prerelease__mutmut_33,
        "xǁVersionResolverǁis_prerelease__mutmut_34": xǁVersionResolverǁis_prerelease__mutmut_34,
        "xǁVersionResolverǁis_prerelease__mutmut_35": xǁVersionResolverǁis_prerelease__mutmut_35,
        "xǁVersionResolverǁis_prerelease__mutmut_36": xǁVersionResolverǁis_prerelease__mutmut_36,
        "xǁVersionResolverǁis_prerelease__mutmut_37": xǁVersionResolverǁis_prerelease__mutmut_37,
        "xǁVersionResolverǁis_prerelease__mutmut_38": xǁVersionResolverǁis_prerelease__mutmut_38,
        "xǁVersionResolverǁis_prerelease__mutmut_39": xǁVersionResolverǁis_prerelease__mutmut_39,
        "xǁVersionResolverǁis_prerelease__mutmut_40": xǁVersionResolverǁis_prerelease__mutmut_40,
        "xǁVersionResolverǁis_prerelease__mutmut_41": xǁVersionResolverǁis_prerelease__mutmut_41,
    }

    def is_prerelease(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁVersionResolverǁis_prerelease__mutmut_orig"),
            object.__getattribute__(self, "xǁVersionResolverǁis_prerelease__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    is_prerelease.__signature__ = _mutmut_signature(xǁVersionResolverǁis_prerelease__mutmut_orig)
    xǁVersionResolverǁis_prerelease__mutmut_orig.__name__ = "xǁVersionResolverǁis_prerelease"

    def xǁVersionResolverǁresolve_tilde__mutmut_orig(self, base: str, available: list[str]) -> str | None:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_1(self, base: str, available: list[str]) -> str | None:
        """Resolve tilde range (~1.2.3 means >=1.2.3 <1.3.0).

        Args:
            base: Base version without tilde.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        try:
            parts = None
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

    def xǁVersionResolverǁresolve_tilde__mutmut_2(self, base: str, available: list[str]) -> str | None:
        """Resolve tilde range (~1.2.3 means >=1.2.3 <1.3.0).

        Args:
            base: Base version without tilde.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        try:
            parts = self.parse_version(None)
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

    def xǁVersionResolverǁresolve_tilde__mutmut_3(self, base: str, available: list[str]) -> str | None:
        """Resolve tilde range (~1.2.3 means >=1.2.3 <1.3.0).

        Args:
            base: Base version without tilde.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        try:
            parts = self.parse_version(base)
            if len(parts) <= 2:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_4(self, base: str, available: list[str]) -> str | None:
        """Resolve tilde range (~1.2.3 means >=1.2.3 <1.3.0).

        Args:
            base: Base version without tilde.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        try:
            parts = self.parse_version(base)
            if len(parts) < 3:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_5(self, base: str, available: list[str]) -> str | None:
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

            major, minor = None

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

    def xǁVersionResolverǁresolve_tilde__mutmut_6(self, base: str, available: list[str]) -> str | None:
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

            major, minor = parts[1], parts[1]

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

    def xǁVersionResolverǁresolve_tilde__mutmut_7(self, base: str, available: list[str]) -> str | None:
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

            major, minor = parts[0], parts[2]

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

    def xǁVersionResolverǁresolve_tilde__mutmut_8(self, base: str, available: list[str]) -> str | None:
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
            matches = None
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

    def xǁVersionResolverǁresolve_tilde__mutmut_9(self, base: str, available: list[str]) -> str | None:
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
                v_parts = None
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

    def xǁVersionResolverǁresolve_tilde__mutmut_10(self, base: str, available: list[str]) -> str | None:
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
                v_parts = self.parse_version(None)
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

    def xǁVersionResolverǁresolve_tilde__mutmut_11(self, base: str, available: list[str]) -> str | None:
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
                if len(v_parts) >= 2 and v_parts[0] == major or v_parts[1] == minor:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_12(self, base: str, available: list[str]) -> str | None:
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
                if len(v_parts) >= 2 or v_parts[0] == major and v_parts[1] == minor:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_13(self, base: str, available: list[str]) -> str | None:
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
                if len(v_parts) > 2 and v_parts[0] == major and v_parts[1] == minor:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_14(self, base: str, available: list[str]) -> str | None:
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
                if len(v_parts) >= 3 and v_parts[0] == major and v_parts[1] == minor:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_15(self, base: str, available: list[str]) -> str | None:
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
                if len(v_parts) >= 2 and v_parts[1] == major and v_parts[1] == minor:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_16(self, base: str, available: list[str]) -> str | None:
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
                if len(v_parts) >= 2 and v_parts[0] != major and v_parts[1] == minor:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_17(self, base: str, available: list[str]) -> str | None:
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
                if len(v_parts) >= 2 and v_parts[0] == major and v_parts[2] == minor:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_18(self, base: str, available: list[str]) -> str | None:
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
                if len(v_parts) >= 2 and v_parts[0] == major and v_parts[1] != minor:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_19(self, base: str, available: list[str]) -> str | None:
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
                    if len(parts) > 3:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_20(self, base: str, available: list[str]) -> str | None:
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
                    if len(parts) >= 4:
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

    def xǁVersionResolverǁresolve_tilde__mutmut_21(self, base: str, available: list[str]) -> str | None:
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
                        if len(v_parts) >= 3 or v_parts[2] >= parts[2]:
                            matches.append(v)
                    else:
                        matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve tilde range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_tilde__mutmut_22(self, base: str, available: list[str]) -> str | None:
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
                        if len(v_parts) > 3 and v_parts[2] >= parts[2]:
                            matches.append(v)
                    else:
                        matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve tilde range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_tilde__mutmut_23(self, base: str, available: list[str]) -> str | None:
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
                        if len(v_parts) >= 4 and v_parts[2] >= parts[2]:
                            matches.append(v)
                    else:
                        matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve tilde range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_tilde__mutmut_24(self, base: str, available: list[str]) -> str | None:
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
                        if len(v_parts) >= 3 and v_parts[3] >= parts[2]:
                            matches.append(v)
                    else:
                        matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve tilde range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_tilde__mutmut_25(self, base: str, available: list[str]) -> str | None:
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
                        if len(v_parts) >= 3 and v_parts[2] > parts[2]:
                            matches.append(v)
                    else:
                        matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve tilde range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_tilde__mutmut_26(self, base: str, available: list[str]) -> str | None:
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
                        if len(v_parts) >= 3 and v_parts[2] >= parts[3]:
                            matches.append(v)
                    else:
                        matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve tilde range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_tilde__mutmut_27(self, base: str, available: list[str]) -> str | None:
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
                            matches.append(None)
                    else:
                        matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve tilde range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_tilde__mutmut_28(self, base: str, available: list[str]) -> str | None:
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
                        matches.append(None)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve tilde range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_tilde__mutmut_29(self, base: str, available: list[str]) -> str | None:
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
                return self.sort_versions(None)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve tilde range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_tilde__mutmut_30(self, base: str, available: list[str]) -> str | None:
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
                return self.sort_versions(matches)[+1]
        except Exception as e:
            log.debug(f"Failed to resolve tilde range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_tilde__mutmut_31(self, base: str, available: list[str]) -> str | None:
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
                return self.sort_versions(matches)[-2]
        except Exception as e:
            log.debug(f"Failed to resolve tilde range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_tilde__mutmut_32(self, base: str, available: list[str]) -> str | None:
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
            log.debug(None)

        return None

    xǁVersionResolverǁresolve_tilde__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁVersionResolverǁresolve_tilde__mutmut_1": xǁVersionResolverǁresolve_tilde__mutmut_1,
        "xǁVersionResolverǁresolve_tilde__mutmut_2": xǁVersionResolverǁresolve_tilde__mutmut_2,
        "xǁVersionResolverǁresolve_tilde__mutmut_3": xǁVersionResolverǁresolve_tilde__mutmut_3,
        "xǁVersionResolverǁresolve_tilde__mutmut_4": xǁVersionResolverǁresolve_tilde__mutmut_4,
        "xǁVersionResolverǁresolve_tilde__mutmut_5": xǁVersionResolverǁresolve_tilde__mutmut_5,
        "xǁVersionResolverǁresolve_tilde__mutmut_6": xǁVersionResolverǁresolve_tilde__mutmut_6,
        "xǁVersionResolverǁresolve_tilde__mutmut_7": xǁVersionResolverǁresolve_tilde__mutmut_7,
        "xǁVersionResolverǁresolve_tilde__mutmut_8": xǁVersionResolverǁresolve_tilde__mutmut_8,
        "xǁVersionResolverǁresolve_tilde__mutmut_9": xǁVersionResolverǁresolve_tilde__mutmut_9,
        "xǁVersionResolverǁresolve_tilde__mutmut_10": xǁVersionResolverǁresolve_tilde__mutmut_10,
        "xǁVersionResolverǁresolve_tilde__mutmut_11": xǁVersionResolverǁresolve_tilde__mutmut_11,
        "xǁVersionResolverǁresolve_tilde__mutmut_12": xǁVersionResolverǁresolve_tilde__mutmut_12,
        "xǁVersionResolverǁresolve_tilde__mutmut_13": xǁVersionResolverǁresolve_tilde__mutmut_13,
        "xǁVersionResolverǁresolve_tilde__mutmut_14": xǁVersionResolverǁresolve_tilde__mutmut_14,
        "xǁVersionResolverǁresolve_tilde__mutmut_15": xǁVersionResolverǁresolve_tilde__mutmut_15,
        "xǁVersionResolverǁresolve_tilde__mutmut_16": xǁVersionResolverǁresolve_tilde__mutmut_16,
        "xǁVersionResolverǁresolve_tilde__mutmut_17": xǁVersionResolverǁresolve_tilde__mutmut_17,
        "xǁVersionResolverǁresolve_tilde__mutmut_18": xǁVersionResolverǁresolve_tilde__mutmut_18,
        "xǁVersionResolverǁresolve_tilde__mutmut_19": xǁVersionResolverǁresolve_tilde__mutmut_19,
        "xǁVersionResolverǁresolve_tilde__mutmut_20": xǁVersionResolverǁresolve_tilde__mutmut_20,
        "xǁVersionResolverǁresolve_tilde__mutmut_21": xǁVersionResolverǁresolve_tilde__mutmut_21,
        "xǁVersionResolverǁresolve_tilde__mutmut_22": xǁVersionResolverǁresolve_tilde__mutmut_22,
        "xǁVersionResolverǁresolve_tilde__mutmut_23": xǁVersionResolverǁresolve_tilde__mutmut_23,
        "xǁVersionResolverǁresolve_tilde__mutmut_24": xǁVersionResolverǁresolve_tilde__mutmut_24,
        "xǁVersionResolverǁresolve_tilde__mutmut_25": xǁVersionResolverǁresolve_tilde__mutmut_25,
        "xǁVersionResolverǁresolve_tilde__mutmut_26": xǁVersionResolverǁresolve_tilde__mutmut_26,
        "xǁVersionResolverǁresolve_tilde__mutmut_27": xǁVersionResolverǁresolve_tilde__mutmut_27,
        "xǁVersionResolverǁresolve_tilde__mutmut_28": xǁVersionResolverǁresolve_tilde__mutmut_28,
        "xǁVersionResolverǁresolve_tilde__mutmut_29": xǁVersionResolverǁresolve_tilde__mutmut_29,
        "xǁVersionResolverǁresolve_tilde__mutmut_30": xǁVersionResolverǁresolve_tilde__mutmut_30,
        "xǁVersionResolverǁresolve_tilde__mutmut_31": xǁVersionResolverǁresolve_tilde__mutmut_31,
        "xǁVersionResolverǁresolve_tilde__mutmut_32": xǁVersionResolverǁresolve_tilde__mutmut_32,
    }

    def resolve_tilde(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁVersionResolverǁresolve_tilde__mutmut_orig"),
            object.__getattribute__(self, "xǁVersionResolverǁresolve_tilde__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    resolve_tilde.__signature__ = _mutmut_signature(xǁVersionResolverǁresolve_tilde__mutmut_orig)
    xǁVersionResolverǁresolve_tilde__mutmut_orig.__name__ = "xǁVersionResolverǁresolve_tilde"

    def xǁVersionResolverǁresolve_caret__mutmut_orig(self, base: str, available: list[str]) -> str | None:
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

    def xǁVersionResolverǁresolve_caret__mutmut_1(self, base: str, available: list[str]) -> str | None:
        """Resolve caret range (^1.2.3 means >=1.2.3 <2.0.0).

        Args:
            base: Base version without caret.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        try:
            parts = None
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

    def xǁVersionResolverǁresolve_caret__mutmut_2(self, base: str, available: list[str]) -> str | None:
        """Resolve caret range (^1.2.3 means >=1.2.3 <2.0.0).

        Args:
            base: Base version without caret.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        try:
            parts = self.parse_version(None)
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

    def xǁVersionResolverǁresolve_caret__mutmut_3(self, base: str, available: list[str]) -> str | None:
        """Resolve caret range (^1.2.3 means >=1.2.3 <2.0.0).

        Args:
            base: Base version without caret.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        try:
            parts = self.parse_version(base)
            if parts:
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

    def xǁVersionResolverǁresolve_caret__mutmut_4(self, base: str, available: list[str]) -> str | None:
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

            major = None

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

    def xǁVersionResolverǁresolve_caret__mutmut_5(self, base: str, available: list[str]) -> str | None:
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

            major = parts[1]

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

    def xǁVersionResolverǁresolve_caret__mutmut_6(self, base: str, available: list[str]) -> str | None:
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
            matches = None
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

    def xǁVersionResolverǁresolve_caret__mutmut_7(self, base: str, available: list[str]) -> str | None:
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
                v_parts = None
                if v_parts and v_parts[0] == major and self.compare_versions(v, base) >= 0:
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_8(self, base: str, available: list[str]) -> str | None:
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
                v_parts = self.parse_version(None)
                if v_parts and v_parts[0] == major and self.compare_versions(v, base) >= 0:
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_9(self, base: str, available: list[str]) -> str | None:
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
                if v_parts and v_parts[0] == major or self.compare_versions(v, base) >= 0:
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_10(self, base: str, available: list[str]) -> str | None:
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
                if v_parts or v_parts[0] == major and self.compare_versions(v, base) >= 0:
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_11(self, base: str, available: list[str]) -> str | None:
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
                if v_parts and v_parts[1] == major and self.compare_versions(v, base) >= 0:
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_12(self, base: str, available: list[str]) -> str | None:
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
                if v_parts and v_parts[0] != major and self.compare_versions(v, base) >= 0:
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_13(self, base: str, available: list[str]) -> str | None:
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
                if v_parts and v_parts[0] == major and self.compare_versions(None, base) >= 0:
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_14(self, base: str, available: list[str]) -> str | None:
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
                if v_parts and v_parts[0] == major and self.compare_versions(v, None) >= 0:
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_15(self, base: str, available: list[str]) -> str | None:
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
                if v_parts and v_parts[0] == major and self.compare_versions(base) >= 0:
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_16(self, base: str, available: list[str]) -> str | None:
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
                if (
                    v_parts
                    and v_parts[0] == major
                    and self.compare_versions(
                        v,
                    )
                    >= 0
                ):
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_17(self, base: str, available: list[str]) -> str | None:
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
                if v_parts and v_parts[0] == major and self.compare_versions(v, base) > 0:
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_18(self, base: str, available: list[str]) -> str | None:
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
                if v_parts and v_parts[0] == major and self.compare_versions(v, base) >= 1:
                    # Must be >= base version
                    matches.append(v)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_19(self, base: str, available: list[str]) -> str | None:
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
                    matches.append(None)

            if matches:
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_20(self, base: str, available: list[str]) -> str | None:
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
                return self.sort_versions(None)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_21(self, base: str, available: list[str]) -> str | None:
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
                return self.sort_versions(matches)[+1]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_22(self, base: str, available: list[str]) -> str | None:
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
                return self.sort_versions(matches)[-2]
        except Exception as e:
            log.debug(f"Failed to resolve caret range {base}: {e}")

        return None

    def xǁVersionResolverǁresolve_caret__mutmut_23(self, base: str, available: list[str]) -> str | None:
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
            log.debug(None)

        return None

    xǁVersionResolverǁresolve_caret__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁVersionResolverǁresolve_caret__mutmut_1": xǁVersionResolverǁresolve_caret__mutmut_1,
        "xǁVersionResolverǁresolve_caret__mutmut_2": xǁVersionResolverǁresolve_caret__mutmut_2,
        "xǁVersionResolverǁresolve_caret__mutmut_3": xǁVersionResolverǁresolve_caret__mutmut_3,
        "xǁVersionResolverǁresolve_caret__mutmut_4": xǁVersionResolverǁresolve_caret__mutmut_4,
        "xǁVersionResolverǁresolve_caret__mutmut_5": xǁVersionResolverǁresolve_caret__mutmut_5,
        "xǁVersionResolverǁresolve_caret__mutmut_6": xǁVersionResolverǁresolve_caret__mutmut_6,
        "xǁVersionResolverǁresolve_caret__mutmut_7": xǁVersionResolverǁresolve_caret__mutmut_7,
        "xǁVersionResolverǁresolve_caret__mutmut_8": xǁVersionResolverǁresolve_caret__mutmut_8,
        "xǁVersionResolverǁresolve_caret__mutmut_9": xǁVersionResolverǁresolve_caret__mutmut_9,
        "xǁVersionResolverǁresolve_caret__mutmut_10": xǁVersionResolverǁresolve_caret__mutmut_10,
        "xǁVersionResolverǁresolve_caret__mutmut_11": xǁVersionResolverǁresolve_caret__mutmut_11,
        "xǁVersionResolverǁresolve_caret__mutmut_12": xǁVersionResolverǁresolve_caret__mutmut_12,
        "xǁVersionResolverǁresolve_caret__mutmut_13": xǁVersionResolverǁresolve_caret__mutmut_13,
        "xǁVersionResolverǁresolve_caret__mutmut_14": xǁVersionResolverǁresolve_caret__mutmut_14,
        "xǁVersionResolverǁresolve_caret__mutmut_15": xǁVersionResolverǁresolve_caret__mutmut_15,
        "xǁVersionResolverǁresolve_caret__mutmut_16": xǁVersionResolverǁresolve_caret__mutmut_16,
        "xǁVersionResolverǁresolve_caret__mutmut_17": xǁVersionResolverǁresolve_caret__mutmut_17,
        "xǁVersionResolverǁresolve_caret__mutmut_18": xǁVersionResolverǁresolve_caret__mutmut_18,
        "xǁVersionResolverǁresolve_caret__mutmut_19": xǁVersionResolverǁresolve_caret__mutmut_19,
        "xǁVersionResolverǁresolve_caret__mutmut_20": xǁVersionResolverǁresolve_caret__mutmut_20,
        "xǁVersionResolverǁresolve_caret__mutmut_21": xǁVersionResolverǁresolve_caret__mutmut_21,
        "xǁVersionResolverǁresolve_caret__mutmut_22": xǁVersionResolverǁresolve_caret__mutmut_22,
        "xǁVersionResolverǁresolve_caret__mutmut_23": xǁVersionResolverǁresolve_caret__mutmut_23,
    }

    def resolve_caret(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁVersionResolverǁresolve_caret__mutmut_orig"),
            object.__getattribute__(self, "xǁVersionResolverǁresolve_caret__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    resolve_caret.__signature__ = _mutmut_signature(xǁVersionResolverǁresolve_caret__mutmut_orig)
    xǁVersionResolverǁresolve_caret__mutmut_orig.__name__ = "xǁVersionResolverǁresolve_caret"

    def xǁVersionResolverǁresolve_wildcard__mutmut_orig(
        self, pattern: str, available: list[str]
    ) -> str | None:
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_1(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = None
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_2(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(None, r"\.")
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_3(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(".", None)
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_4(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(r"\.")
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_5(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(
            ".",
        )
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_6(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace("XX.XX", r"\.")
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_7(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(".", r"XX\.XX")
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_8(self, pattern: str, available: list[str]) -> str | None:
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_9(self, pattern: str, available: list[str]) -> str | None:
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_10(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(".", r"\.")
        regex_pattern = None
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_11(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(".", r"\.")
        regex_pattern = regex_pattern.replace(None, r".*")
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_12(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(".", r"\.")
        regex_pattern = regex_pattern.replace("*", None)
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_13(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(".", r"\.")
        regex_pattern = regex_pattern.replace(r".*")
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_14(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(".", r"\.")
        regex_pattern = regex_pattern.replace(
            "*",
        )
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_15(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(".", r"\.")
        regex_pattern = regex_pattern.replace("XX*XX", r".*")
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_16(self, pattern: str, available: list[str]) -> str | None:
        """Resolve wildcard pattern (1.2.* matches any 1.2.x).

        Args:
            pattern: Version pattern with wildcards.
            available: List of available versions.

        Returns:
            Best matching version, or None if no match.

        """
        # Convert wildcard to regex (with caching)
        regex_pattern = pattern.replace(".", r"\.")
        regex_pattern = regex_pattern.replace("*", r"XX.*XX")
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_17(self, pattern: str, available: list[str]) -> str | None:
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_18(self, pattern: str, available: list[str]) -> str | None:
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

    def xǁVersionResolverǁresolve_wildcard__mutmut_19(self, pattern: str, available: list[str]) -> str | None:
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
        regex_pattern = None

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

    def xǁVersionResolverǁresolve_wildcard__mutmut_20(self, pattern: str, available: list[str]) -> str | None:
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
            if regex_pattern in self._pattern_cache:
                self._pattern_cache[regex_pattern] = re.compile(regex_pattern)

            regex = self._pattern_cache[regex_pattern]
            matches = [v for v in available if regex.match(v)]

            if matches:
                # Return latest matching version
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve wildcard {pattern}: {e}")

        return None

    def xǁVersionResolverǁresolve_wildcard__mutmut_21(self, pattern: str, available: list[str]) -> str | None:
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
                self._pattern_cache[regex_pattern] = None

            regex = self._pattern_cache[regex_pattern]
            matches = [v for v in available if regex.match(v)]

            if matches:
                # Return latest matching version
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve wildcard {pattern}: {e}")

        return None

    def xǁVersionResolverǁresolve_wildcard__mutmut_22(self, pattern: str, available: list[str]) -> str | None:
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
                self._pattern_cache[regex_pattern] = re.compile(None)

            regex = self._pattern_cache[regex_pattern]
            matches = [v for v in available if regex.match(v)]

            if matches:
                # Return latest matching version
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve wildcard {pattern}: {e}")

        return None

    def xǁVersionResolverǁresolve_wildcard__mutmut_23(self, pattern: str, available: list[str]) -> str | None:
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

            regex = None
            matches = [v for v in available if regex.match(v)]

            if matches:
                # Return latest matching version
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve wildcard {pattern}: {e}")

        return None

    def xǁVersionResolverǁresolve_wildcard__mutmut_24(self, pattern: str, available: list[str]) -> str | None:
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
            matches = None

            if matches:
                # Return latest matching version
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve wildcard {pattern}: {e}")

        return None

    def xǁVersionResolverǁresolve_wildcard__mutmut_25(self, pattern: str, available: list[str]) -> str | None:
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
            matches = [v for v in available if regex.match(None)]

            if matches:
                # Return latest matching version
                return self.sort_versions(matches)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve wildcard {pattern}: {e}")

        return None

    def xǁVersionResolverǁresolve_wildcard__mutmut_26(self, pattern: str, available: list[str]) -> str | None:
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
                return self.sort_versions(None)[-1]
        except Exception as e:
            log.debug(f"Failed to resolve wildcard {pattern}: {e}")

        return None

    def xǁVersionResolverǁresolve_wildcard__mutmut_27(self, pattern: str, available: list[str]) -> str | None:
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
                return self.sort_versions(matches)[+1]
        except Exception as e:
            log.debug(f"Failed to resolve wildcard {pattern}: {e}")

        return None

    def xǁVersionResolverǁresolve_wildcard__mutmut_28(self, pattern: str, available: list[str]) -> str | None:
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
                return self.sort_versions(matches)[-2]
        except Exception as e:
            log.debug(f"Failed to resolve wildcard {pattern}: {e}")

        return None

    def xǁVersionResolverǁresolve_wildcard__mutmut_29(self, pattern: str, available: list[str]) -> str | None:
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
            log.debug(None)

        return None

    xǁVersionResolverǁresolve_wildcard__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁVersionResolverǁresolve_wildcard__mutmut_1": xǁVersionResolverǁresolve_wildcard__mutmut_1,
        "xǁVersionResolverǁresolve_wildcard__mutmut_2": xǁVersionResolverǁresolve_wildcard__mutmut_2,
        "xǁVersionResolverǁresolve_wildcard__mutmut_3": xǁVersionResolverǁresolve_wildcard__mutmut_3,
        "xǁVersionResolverǁresolve_wildcard__mutmut_4": xǁVersionResolverǁresolve_wildcard__mutmut_4,
        "xǁVersionResolverǁresolve_wildcard__mutmut_5": xǁVersionResolverǁresolve_wildcard__mutmut_5,
        "xǁVersionResolverǁresolve_wildcard__mutmut_6": xǁVersionResolverǁresolve_wildcard__mutmut_6,
        "xǁVersionResolverǁresolve_wildcard__mutmut_7": xǁVersionResolverǁresolve_wildcard__mutmut_7,
        "xǁVersionResolverǁresolve_wildcard__mutmut_8": xǁVersionResolverǁresolve_wildcard__mutmut_8,
        "xǁVersionResolverǁresolve_wildcard__mutmut_9": xǁVersionResolverǁresolve_wildcard__mutmut_9,
        "xǁVersionResolverǁresolve_wildcard__mutmut_10": xǁVersionResolverǁresolve_wildcard__mutmut_10,
        "xǁVersionResolverǁresolve_wildcard__mutmut_11": xǁVersionResolverǁresolve_wildcard__mutmut_11,
        "xǁVersionResolverǁresolve_wildcard__mutmut_12": xǁVersionResolverǁresolve_wildcard__mutmut_12,
        "xǁVersionResolverǁresolve_wildcard__mutmut_13": xǁVersionResolverǁresolve_wildcard__mutmut_13,
        "xǁVersionResolverǁresolve_wildcard__mutmut_14": xǁVersionResolverǁresolve_wildcard__mutmut_14,
        "xǁVersionResolverǁresolve_wildcard__mutmut_15": xǁVersionResolverǁresolve_wildcard__mutmut_15,
        "xǁVersionResolverǁresolve_wildcard__mutmut_16": xǁVersionResolverǁresolve_wildcard__mutmut_16,
        "xǁVersionResolverǁresolve_wildcard__mutmut_17": xǁVersionResolverǁresolve_wildcard__mutmut_17,
        "xǁVersionResolverǁresolve_wildcard__mutmut_18": xǁVersionResolverǁresolve_wildcard__mutmut_18,
        "xǁVersionResolverǁresolve_wildcard__mutmut_19": xǁVersionResolverǁresolve_wildcard__mutmut_19,
        "xǁVersionResolverǁresolve_wildcard__mutmut_20": xǁVersionResolverǁresolve_wildcard__mutmut_20,
        "xǁVersionResolverǁresolve_wildcard__mutmut_21": xǁVersionResolverǁresolve_wildcard__mutmut_21,
        "xǁVersionResolverǁresolve_wildcard__mutmut_22": xǁVersionResolverǁresolve_wildcard__mutmut_22,
        "xǁVersionResolverǁresolve_wildcard__mutmut_23": xǁVersionResolverǁresolve_wildcard__mutmut_23,
        "xǁVersionResolverǁresolve_wildcard__mutmut_24": xǁVersionResolverǁresolve_wildcard__mutmut_24,
        "xǁVersionResolverǁresolve_wildcard__mutmut_25": xǁVersionResolverǁresolve_wildcard__mutmut_25,
        "xǁVersionResolverǁresolve_wildcard__mutmut_26": xǁVersionResolverǁresolve_wildcard__mutmut_26,
        "xǁVersionResolverǁresolve_wildcard__mutmut_27": xǁVersionResolverǁresolve_wildcard__mutmut_27,
        "xǁVersionResolverǁresolve_wildcard__mutmut_28": xǁVersionResolverǁresolve_wildcard__mutmut_28,
        "xǁVersionResolverǁresolve_wildcard__mutmut_29": xǁVersionResolverǁresolve_wildcard__mutmut_29,
    }

    def resolve_wildcard(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁVersionResolverǁresolve_wildcard__mutmut_orig"),
            object.__getattribute__(self, "xǁVersionResolverǁresolve_wildcard__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    resolve_wildcard.__signature__ = _mutmut_signature(xǁVersionResolverǁresolve_wildcard__mutmut_orig)
    xǁVersionResolverǁresolve_wildcard__mutmut_orig.__name__ = "xǁVersionResolverǁresolve_wildcard"

    def xǁVersionResolverǁparse_version__mutmut_orig(self, version: str) -> list[int]:
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

    def xǁVersionResolverǁparse_version__mutmut_1(self, version: str) -> list[int]:
        """Parse version string into numeric components.

        Args:
            version: Version string.

        Returns:
            List of numeric version components.

        """
        # Extract just the numeric version part
        match = None
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

    def xǁVersionResolverǁparse_version__mutmut_2(self, version: str) -> list[int]:
        """Parse version string into numeric components.

        Args:
            version: Version string.

        Returns:
            List of numeric version components.

        """
        # Extract just the numeric version part
        match = re.match(None, version)
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

    def xǁVersionResolverǁparse_version__mutmut_3(self, version: str) -> list[int]:
        """Parse version string into numeric components.

        Args:
            version: Version string.

        Returns:
            List of numeric version components.

        """
        # Extract just the numeric version part
        match = re.match(r"^v?(\d+(?:\.\d+)*)", None)
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

    def xǁVersionResolverǁparse_version__mutmut_4(self, version: str) -> list[int]:
        """Parse version string into numeric components.

        Args:
            version: Version string.

        Returns:
            List of numeric version components.

        """
        # Extract just the numeric version part
        match = re.match(version)
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

    def xǁVersionResolverǁparse_version__mutmut_5(self, version: str) -> list[int]:
        """Parse version string into numeric components.

        Args:
            version: Version string.

        Returns:
            List of numeric version components.

        """
        # Extract just the numeric version part
        match = re.match(
            r"^v?(\d+(?:\.\d+)*)",
        )
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

    def xǁVersionResolverǁparse_version__mutmut_6(self, version: str) -> list[int]:
        """Parse version string into numeric components.

        Args:
            version: Version string.

        Returns:
            List of numeric version components.

        """
        # Extract just the numeric version part
        match = re.match(r"XX^v?(\d+(?:\.\d+)*)XX", version)
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

    def xǁVersionResolverǁparse_version__mutmut_7(self, version: str) -> list[int]:
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

    def xǁVersionResolverǁparse_version__mutmut_8(self, version: str) -> list[int]:
        """Parse version string into numeric components.

        Args:
            version: Version string.

        Returns:
            List of numeric version components.

        """
        # Extract just the numeric version part
        match = re.match(r"^V?(\d+(?:\.\d+)*)", version)
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

    def xǁVersionResolverǁparse_version__mutmut_9(self, version: str) -> list[int]:
        """Parse version string into numeric components.

        Args:
            version: Version string.

        Returns:
            List of numeric version components.

        """
        # Extract just the numeric version part
        match = re.match(r"^v?(\d+(?:\.\d+)*)", version)
        if match:
            return []

        version_str = match.group(1)
        parts = []

        for part in version_str.split("."):
            try:
                parts.append(int(part))
            except ValueError:
                break

        return parts

    def xǁVersionResolverǁparse_version__mutmut_10(self, version: str) -> list[int]:
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

        version_str = None
        parts = []

        for part in version_str.split("."):
            try:
                parts.append(int(part))
            except ValueError:
                break

        return parts

    def xǁVersionResolverǁparse_version__mutmut_11(self, version: str) -> list[int]:
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

        version_str = match.group(None)
        parts = []

        for part in version_str.split("."):
            try:
                parts.append(int(part))
            except ValueError:
                break

        return parts

    def xǁVersionResolverǁparse_version__mutmut_12(self, version: str) -> list[int]:
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

        version_str = match.group(2)
        parts = []

        for part in version_str.split("."):
            try:
                parts.append(int(part))
            except ValueError:
                break

        return parts

    def xǁVersionResolverǁparse_version__mutmut_13(self, version: str) -> list[int]:
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
        parts = None

        for part in version_str.split("."):
            try:
                parts.append(int(part))
            except ValueError:
                break

        return parts

    def xǁVersionResolverǁparse_version__mutmut_14(self, version: str) -> list[int]:
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

        for part in version_str.split(None):
            try:
                parts.append(int(part))
            except ValueError:
                break

        return parts

    def xǁVersionResolverǁparse_version__mutmut_15(self, version: str) -> list[int]:
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

        for part in version_str.split("XX.XX"):
            try:
                parts.append(int(part))
            except ValueError:
                break

        return parts

    def xǁVersionResolverǁparse_version__mutmut_16(self, version: str) -> list[int]:
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
                parts.append(None)
            except ValueError:
                break

        return parts

    def xǁVersionResolverǁparse_version__mutmut_17(self, version: str) -> list[int]:
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
                parts.append(int(None))
            except ValueError:
                break

        return parts

    def xǁVersionResolverǁparse_version__mutmut_18(self, version: str) -> list[int]:
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
                return

        return parts

    xǁVersionResolverǁparse_version__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁVersionResolverǁparse_version__mutmut_1": xǁVersionResolverǁparse_version__mutmut_1,
        "xǁVersionResolverǁparse_version__mutmut_2": xǁVersionResolverǁparse_version__mutmut_2,
        "xǁVersionResolverǁparse_version__mutmut_3": xǁVersionResolverǁparse_version__mutmut_3,
        "xǁVersionResolverǁparse_version__mutmut_4": xǁVersionResolverǁparse_version__mutmut_4,
        "xǁVersionResolverǁparse_version__mutmut_5": xǁVersionResolverǁparse_version__mutmut_5,
        "xǁVersionResolverǁparse_version__mutmut_6": xǁVersionResolverǁparse_version__mutmut_6,
        "xǁVersionResolverǁparse_version__mutmut_7": xǁVersionResolverǁparse_version__mutmut_7,
        "xǁVersionResolverǁparse_version__mutmut_8": xǁVersionResolverǁparse_version__mutmut_8,
        "xǁVersionResolverǁparse_version__mutmut_9": xǁVersionResolverǁparse_version__mutmut_9,
        "xǁVersionResolverǁparse_version__mutmut_10": xǁVersionResolverǁparse_version__mutmut_10,
        "xǁVersionResolverǁparse_version__mutmut_11": xǁVersionResolverǁparse_version__mutmut_11,
        "xǁVersionResolverǁparse_version__mutmut_12": xǁVersionResolverǁparse_version__mutmut_12,
        "xǁVersionResolverǁparse_version__mutmut_13": xǁVersionResolverǁparse_version__mutmut_13,
        "xǁVersionResolverǁparse_version__mutmut_14": xǁVersionResolverǁparse_version__mutmut_14,
        "xǁVersionResolverǁparse_version__mutmut_15": xǁVersionResolverǁparse_version__mutmut_15,
        "xǁVersionResolverǁparse_version__mutmut_16": xǁVersionResolverǁparse_version__mutmut_16,
        "xǁVersionResolverǁparse_version__mutmut_17": xǁVersionResolverǁparse_version__mutmut_17,
        "xǁVersionResolverǁparse_version__mutmut_18": xǁVersionResolverǁparse_version__mutmut_18,
    }

    def parse_version(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁVersionResolverǁparse_version__mutmut_orig"),
            object.__getattribute__(self, "xǁVersionResolverǁparse_version__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    parse_version.__signature__ = _mutmut_signature(xǁVersionResolverǁparse_version__mutmut_orig)
    xǁVersionResolverǁparse_version__mutmut_orig.__name__ = "xǁVersionResolverǁparse_version"

    def xǁVersionResolverǁcompare_versions__mutmut_orig(self, v1: str, v2: str) -> int:
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

    def xǁVersionResolverǁcompare_versions__mutmut_1(self, v1: str, v2: str) -> int:
        """Compare two versions.

        Args:
            v1: First version.
            v2: Second version.

        Returns:
            -1 if v1 < v2, 0 if equal, 1 if v1 > v2.

        """
        parts1 = None
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

    def xǁVersionResolverǁcompare_versions__mutmut_2(self, v1: str, v2: str) -> int:
        """Compare two versions.

        Args:
            v1: First version.
            v2: Second version.

        Returns:
            -1 if v1 < v2, 0 if equal, 1 if v1 > v2.

        """
        parts1 = self.parse_version(None)
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

    def xǁVersionResolverǁcompare_versions__mutmut_3(self, v1: str, v2: str) -> int:
        """Compare two versions.

        Args:
            v1: First version.
            v2: Second version.

        Returns:
            -1 if v1 < v2, 0 if equal, 1 if v1 > v2.

        """
        parts1 = self.parse_version(v1)
        parts2 = None

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

    def xǁVersionResolverǁcompare_versions__mutmut_4(self, v1: str, v2: str) -> int:
        """Compare two versions.

        Args:
            v1: First version.
            v2: Second version.

        Returns:
            -1 if v1 < v2, 0 if equal, 1 if v1 > v2.

        """
        parts1 = self.parse_version(v1)
        parts2 = self.parse_version(None)

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

    def xǁVersionResolverǁcompare_versions__mutmut_5(self, v1: str, v2: str) -> int:
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
        max_len = None
        parts1.extend([0] * (max_len - len(parts1)))
        parts2.extend([0] * (max_len - len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_6(self, v1: str, v2: str) -> int:
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
        max_len = max(None, len(parts2))
        parts1.extend([0] * (max_len - len(parts1)))
        parts2.extend([0] * (max_len - len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_7(self, v1: str, v2: str) -> int:
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
        max_len = max(len(parts1), None)
        parts1.extend([0] * (max_len - len(parts1)))
        parts2.extend([0] * (max_len - len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_8(self, v1: str, v2: str) -> int:
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
        max_len = max(len(parts2))
        parts1.extend([0] * (max_len - len(parts1)))
        parts2.extend([0] * (max_len - len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_9(self, v1: str, v2: str) -> int:
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
        max_len = max(
            len(parts1),
        )
        parts1.extend([0] * (max_len - len(parts1)))
        parts2.extend([0] * (max_len - len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_10(self, v1: str, v2: str) -> int:
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
        parts1.extend(None)
        parts2.extend([0] * (max_len - len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_11(self, v1: str, v2: str) -> int:
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
        parts1.extend([0] / (max_len - len(parts1)))
        parts2.extend([0] * (max_len - len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_12(self, v1: str, v2: str) -> int:
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
        parts1.extend([1] * (max_len - len(parts1)))
        parts2.extend([0] * (max_len - len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_13(self, v1: str, v2: str) -> int:
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
        parts1.extend([0] * (max_len + len(parts1)))
        parts2.extend([0] * (max_len - len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_14(self, v1: str, v2: str) -> int:
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
        parts2.extend(None)

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_15(self, v1: str, v2: str) -> int:
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
        parts2.extend([0] / (max_len - len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_16(self, v1: str, v2: str) -> int:
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
        parts2.extend([1] * (max_len - len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_17(self, v1: str, v2: str) -> int:
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
        parts2.extend([0] * (max_len + len(parts2)))

        for p1, p2 in zip(parts1, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_18(self, v1: str, v2: str) -> int:
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

        for p1, p2 in zip(None, parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_19(self, v1: str, v2: str) -> int:
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

        for p1, p2 in zip(parts1, None, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_20(self, v1: str, v2: str) -> int:
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

        for p1, p2 in zip(parts1, parts2, strict=None):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_21(self, v1: str, v2: str) -> int:
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

        for p1, p2 in zip(parts2, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_22(self, v1: str, v2: str) -> int:
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

        for p1, p2 in zip(parts1, strict=False):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_23(self, v1: str, v2: str) -> int:
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

        for p1, p2 in zip(
            parts1,
            parts2,
        ):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_24(self, v1: str, v2: str) -> int:
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

        for p1, p2 in zip(parts1, parts2, strict=True):
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_25(self, v1: str, v2: str) -> int:
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
            if p1 <= p2:
                return -1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_26(self, v1: str, v2: str) -> int:
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
                return +1
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_27(self, v1: str, v2: str) -> int:
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
                return -2
            if p1 > p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_28(self, v1: str, v2: str) -> int:
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
            if p1 >= p2:
                return 1

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_29(self, v1: str, v2: str) -> int:
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
                return 2

        return 0

    def xǁVersionResolverǁcompare_versions__mutmut_30(self, v1: str, v2: str) -> int:
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

        return 1

    xǁVersionResolverǁcompare_versions__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁVersionResolverǁcompare_versions__mutmut_1": xǁVersionResolverǁcompare_versions__mutmut_1,
        "xǁVersionResolverǁcompare_versions__mutmut_2": xǁVersionResolverǁcompare_versions__mutmut_2,
        "xǁVersionResolverǁcompare_versions__mutmut_3": xǁVersionResolverǁcompare_versions__mutmut_3,
        "xǁVersionResolverǁcompare_versions__mutmut_4": xǁVersionResolverǁcompare_versions__mutmut_4,
        "xǁVersionResolverǁcompare_versions__mutmut_5": xǁVersionResolverǁcompare_versions__mutmut_5,
        "xǁVersionResolverǁcompare_versions__mutmut_6": xǁVersionResolverǁcompare_versions__mutmut_6,
        "xǁVersionResolverǁcompare_versions__mutmut_7": xǁVersionResolverǁcompare_versions__mutmut_7,
        "xǁVersionResolverǁcompare_versions__mutmut_8": xǁVersionResolverǁcompare_versions__mutmut_8,
        "xǁVersionResolverǁcompare_versions__mutmut_9": xǁVersionResolverǁcompare_versions__mutmut_9,
        "xǁVersionResolverǁcompare_versions__mutmut_10": xǁVersionResolverǁcompare_versions__mutmut_10,
        "xǁVersionResolverǁcompare_versions__mutmut_11": xǁVersionResolverǁcompare_versions__mutmut_11,
        "xǁVersionResolverǁcompare_versions__mutmut_12": xǁVersionResolverǁcompare_versions__mutmut_12,
        "xǁVersionResolverǁcompare_versions__mutmut_13": xǁVersionResolverǁcompare_versions__mutmut_13,
        "xǁVersionResolverǁcompare_versions__mutmut_14": xǁVersionResolverǁcompare_versions__mutmut_14,
        "xǁVersionResolverǁcompare_versions__mutmut_15": xǁVersionResolverǁcompare_versions__mutmut_15,
        "xǁVersionResolverǁcompare_versions__mutmut_16": xǁVersionResolverǁcompare_versions__mutmut_16,
        "xǁVersionResolverǁcompare_versions__mutmut_17": xǁVersionResolverǁcompare_versions__mutmut_17,
        "xǁVersionResolverǁcompare_versions__mutmut_18": xǁVersionResolverǁcompare_versions__mutmut_18,
        "xǁVersionResolverǁcompare_versions__mutmut_19": xǁVersionResolverǁcompare_versions__mutmut_19,
        "xǁVersionResolverǁcompare_versions__mutmut_20": xǁVersionResolverǁcompare_versions__mutmut_20,
        "xǁVersionResolverǁcompare_versions__mutmut_21": xǁVersionResolverǁcompare_versions__mutmut_21,
        "xǁVersionResolverǁcompare_versions__mutmut_22": xǁVersionResolverǁcompare_versions__mutmut_22,
        "xǁVersionResolverǁcompare_versions__mutmut_23": xǁVersionResolverǁcompare_versions__mutmut_23,
        "xǁVersionResolverǁcompare_versions__mutmut_24": xǁVersionResolverǁcompare_versions__mutmut_24,
        "xǁVersionResolverǁcompare_versions__mutmut_25": xǁVersionResolverǁcompare_versions__mutmut_25,
        "xǁVersionResolverǁcompare_versions__mutmut_26": xǁVersionResolverǁcompare_versions__mutmut_26,
        "xǁVersionResolverǁcompare_versions__mutmut_27": xǁVersionResolverǁcompare_versions__mutmut_27,
        "xǁVersionResolverǁcompare_versions__mutmut_28": xǁVersionResolverǁcompare_versions__mutmut_28,
        "xǁVersionResolverǁcompare_versions__mutmut_29": xǁVersionResolverǁcompare_versions__mutmut_29,
        "xǁVersionResolverǁcompare_versions__mutmut_30": xǁVersionResolverǁcompare_versions__mutmut_30,
    }

    def compare_versions(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁVersionResolverǁcompare_versions__mutmut_orig"),
            object.__getattribute__(self, "xǁVersionResolverǁcompare_versions__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    compare_versions.__signature__ = _mutmut_signature(xǁVersionResolverǁcompare_versions__mutmut_orig)
    xǁVersionResolverǁcompare_versions__mutmut_orig.__name__ = "xǁVersionResolverǁcompare_versions"

    def xǁVersionResolverǁsort_versions__mutmut_orig(self, versions: list[str]) -> list[str]:
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

    def xǁVersionResolverǁsort_versions__mutmut_1(self, versions: list[str]) -> list[str]:
        """Sort versions in ascending order.

        Args:
            versions: List of version strings.

        Returns:
            Sorted list of versions.

        """
        return sorted(
            None,
            key=lambda v: (
                self.parse_version(v),
                v,  # Secondary sort by string for pre-releases
            ),
        )

    def xǁVersionResolverǁsort_versions__mutmut_2(self, versions: list[str]) -> list[str]:
        """Sort versions in ascending order.

        Args:
            versions: List of version strings.

        Returns:
            Sorted list of versions.

        """
        return sorted(
            versions,
            key=None,
        )

    def xǁVersionResolverǁsort_versions__mutmut_3(self, versions: list[str]) -> list[str]:
        """Sort versions in ascending order.

        Args:
            versions: List of version strings.

        Returns:
            Sorted list of versions.

        """
        return sorted(
            key=lambda v: (
                self.parse_version(v),
                v,  # Secondary sort by string for pre-releases
            ),
        )

    def xǁVersionResolverǁsort_versions__mutmut_4(self, versions: list[str]) -> list[str]:
        """Sort versions in ascending order.

        Args:
            versions: List of version strings.

        Returns:
            Sorted list of versions.

        """
        return sorted(
            versions,
        )

    def xǁVersionResolverǁsort_versions__mutmut_5(self, versions: list[str]) -> list[str]:
        """Sort versions in ascending order.

        Args:
            versions: List of version strings.

        Returns:
            Sorted list of versions.

        """
        return sorted(
            versions,
            key=lambda v: None,
        )

    def xǁVersionResolverǁsort_versions__mutmut_6(self, versions: list[str]) -> list[str]:
        """Sort versions in ascending order.

        Args:
            versions: List of version strings.

        Returns:
            Sorted list of versions.

        """
        return sorted(
            versions,
            key=lambda v: (
                self.parse_version(None),
                v,  # Secondary sort by string for pre-releases
            ),
        )

    xǁVersionResolverǁsort_versions__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁVersionResolverǁsort_versions__mutmut_1": xǁVersionResolverǁsort_versions__mutmut_1,
        "xǁVersionResolverǁsort_versions__mutmut_2": xǁVersionResolverǁsort_versions__mutmut_2,
        "xǁVersionResolverǁsort_versions__mutmut_3": xǁVersionResolverǁsort_versions__mutmut_3,
        "xǁVersionResolverǁsort_versions__mutmut_4": xǁVersionResolverǁsort_versions__mutmut_4,
        "xǁVersionResolverǁsort_versions__mutmut_5": xǁVersionResolverǁsort_versions__mutmut_5,
        "xǁVersionResolverǁsort_versions__mutmut_6": xǁVersionResolverǁsort_versions__mutmut_6,
    }

    def sort_versions(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁVersionResolverǁsort_versions__mutmut_orig"),
            object.__getattribute__(self, "xǁVersionResolverǁsort_versions__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    sort_versions.__signature__ = _mutmut_signature(xǁVersionResolverǁsort_versions__mutmut_orig)
    xǁVersionResolverǁsort_versions__mutmut_orig.__name__ = "xǁVersionResolverǁsort_versions"


# <3 🧱🤝🔧🪄
