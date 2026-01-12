#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests to achieve full coverage for platform detection and info modules."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest


class TestPlatformDetection(FoundationTestCase):
    """Test platform detection functionality."""

    def setup_method(self) -> None:
        """Set up test environment and clear caches."""
        super().setup_method()
        # Import and clear cached platform detection results before each test
        from provide.foundation.platform.detection import (
            get_arch_name,
            get_cpu_type,
            get_os_name,
            get_os_version,
            get_platform_string,
        )

        get_os_name.cache_clear()  # type: ignore[attr-defined]
        get_arch_name.cache_clear()  # type: ignore[attr-defined]
        get_platform_string.cache_clear()  # type: ignore[attr-defined]
        get_os_version.cache_clear()  # type: ignore[attr-defined]
        get_cpu_type.cache_clear()  # type: ignore[attr-defined]

    def test_get_os_name_darwin(self) -> None:
        """Test OS name detection for Darwin."""
        from provide.foundation.platform.detection import get_os_name

        with patch("platform.system", return_value="Darwin"):
            result = get_os_name()
            assert result == "darwin"

        with patch("platform.system", return_value="MacOS"):
            result = get_os_name()
            assert result == "darwin"

    def test_get_os_name_linux(self) -> None:
        """Test OS name detection for Linux."""
        from provide.foundation.platform.detection import get_os_name

        with patch("platform.system", return_value="Linux"):
            result = get_os_name()
            assert result == "linux"

    def test_get_os_name_windows(self) -> None:
        """Test OS name detection for Windows."""
        from provide.foundation.platform.detection import get_os_name

        with patch("platform.system", return_value="Windows"):
            result = get_os_name()
            assert result == "windows"

    def test_get_os_name_exception_handling(self) -> None:
        """Test OS name detection with exception."""
        from provide.foundation.errors.platform import PlatformError
        from provide.foundation.platform.detection import get_os_name

        with patch("platform.system", side_effect=Exception("Platform error")):
            with pytest.raises(PlatformError) as exc_info:
                get_os_name()

            assert "Failed to detect operating system" in str(exc_info.value)
            assert exc_info.value.code == "PLATFORM_OS_DETECTION_FAILED"

    def test_get_arch_name_amd64_variants(self) -> None:
        """Test architecture detection for amd64 variants."""
        from provide.foundation.platform.detection import get_arch_name

        for arch in ["x86_64", "amd64", "X86_64", "AMD64"]:
            with patch("platform.machine", return_value=arch):
                result = get_arch_name()
                assert result == "amd64"

    def test_get_arch_name_arm64_variants(self) -> None:
        """Test architecture detection for arm64 variants."""
        from provide.foundation.platform.detection import get_arch_name

        for arch in ["aarch64", "arm64", "AARCH64", "ARM64"]:
            with patch("platform.machine", return_value=arch):
                result = get_arch_name()
                assert result == "arm64"

    def test_get_arch_name_x86_variants(self) -> None:
        """Test architecture detection for x86 variants."""
        from provide.foundation.platform.detection import get_arch_name

        for arch in ["i686", "i586", "i486"]:
            with patch("platform.machine", return_value=arch):
                result = get_arch_name()
                assert result == "x86"

    def test_get_arch_name_unknown_arch(self) -> None:
        """Test architecture detection for unknown arch."""
        from provide.foundation.platform.detection import get_arch_name

        with patch("platform.machine", return_value="unknown_arch"):
            result = get_arch_name()
            assert result == "unknown_arch"

    def test_get_arch_name_exception_handling(self) -> None:
        """Test architecture detection with exception."""
        from provide.foundation.errors.platform import PlatformError
        from provide.foundation.platform.detection import get_arch_name

        with patch("platform.machine", side_effect=Exception("Machine error")):
            with pytest.raises(PlatformError) as exc_info:
                get_arch_name()

            assert "Failed to detect architecture" in str(exc_info.value)
            assert exc_info.value.code == "PLATFORM_ARCH_DETECTION_FAILED"

    def test_get_platform_string(self) -> None:
        """Test platform string generation."""
        from provide.foundation.platform.detection import get_platform_string

        result = get_platform_string()
        assert isinstance(result, str)
        assert "_" in result  # Should be format like "darwin_arm64"

        # Test that it includes OS and architecture
        parts = result.split("_")
        assert len(parts) >= 2

    def test_current_platform_detection(self) -> None:
        """Test current platform detection."""
        from provide.foundation.platform.detection import get_platform_string

        # Test that current platform can be detected
        current_platform = get_platform_string()
        assert isinstance(current_platform, str)
        assert len(current_platform.split("_")) >= 2

    def test_get_system_info(self) -> None:
        """Test comprehensive system information."""
        from provide.foundation.platform.info import get_system_info

        result = get_system_info()
        assert result is not None
        assert hasattr(result, "os_name")
        assert hasattr(result, "arch")
        assert hasattr(result, "platform")
        assert hasattr(result, "python_version")
        assert isinstance(result.os_name, str)
        assert isinstance(result.arch, str)


# 🧱🏗️🔚
