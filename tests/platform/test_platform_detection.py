#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for platform detection functions."""

from __future__ import annotations

from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.errors.platform import PlatformError
from provide.foundation.platform.detection import (
    get_arch_name,
    get_cpu_type,
    get_os_name,
    get_os_version,
    get_platform_string,
    normalize_platform_components,
)


class TestPlatformDetection(FoundationTestCase):
    """Test platform detection functions."""

    def setup_method(self) -> None:
        """Set up test environment and clear caches."""
        super().setup_method()
        # Clear cached platform detection results before each test
        get_os_name.cache_clear()  # type: ignore[attr-defined]
        get_arch_name.cache_clear()  # type: ignore[attr-defined]
        get_platform_string.cache_clear()  # type: ignore[attr-defined]
        get_os_version.cache_clear()  # type: ignore[attr-defined]
        get_cpu_type.cache_clear()  # type: ignore[attr-defined]

    def test_get_os_name_normal(self) -> None:
        """Test get_os_name with normal system values."""
        with patch("platform.system") as mock_system:
            # Test Darwin/macOS
            mock_system.return_value = "Darwin"
            assert get_os_name() == "darwin"
            get_os_name.cache_clear()  # type: ignore[attr-defined]

            mock_system.return_value = "Linux"
            assert get_os_name() == "linux"
            get_os_name.cache_clear()  # type: ignore[attr-defined]

            mock_system.return_value = "Windows"
            assert get_os_name() == "windows"

    def test_get_os_name_case_insensitive(self) -> None:
        """Test get_os_name handles case variations."""
        with patch("platform.system") as mock_system:
            mock_system.return_value = "DARWIN"
            assert get_os_name() == "darwin"
            get_os_name.cache_clear()  # type: ignore[attr-defined]

            mock_system.return_value = "linux"
            assert get_os_name() == "linux"

    def test_get_os_name_exception(self) -> None:
        """Test get_os_name raises PlatformError on exception."""
        with patch("platform.system", side_effect=RuntimeError("Test error")):
            with pytest.raises(PlatformError) as exc_info:
                get_os_name()

            assert exc_info.value.code == "PLATFORM_OS_DETECTION_FAILED"
            assert exc_info.value.message == "Failed to detect operating system"

    def test_get_arch_name_x86_variants(self) -> None:
        """Test get_arch_name with x86 variants."""
        with patch("platform.machine") as mock_machine:
            # Test x86_64/amd64
            mock_machine.return_value = "x86_64"
            assert get_arch_name() == "amd64"
            get_arch_name.cache_clear()  # type: ignore[attr-defined]

            mock_machine.return_value = "AMD64"
            assert get_arch_name() == "amd64"
            get_arch_name.cache_clear()  # type: ignore[attr-defined]

            # Test ARM variants
            mock_machine.return_value = "aarch64"
            assert get_arch_name() == "arm64"
            get_arch_name.cache_clear()  # type: ignore[attr-defined]

            mock_machine.return_value = "ARM64"
            assert get_arch_name() == "arm64"
            get_arch_name.cache_clear()  # type: ignore[attr-defined]

            # Test legacy x86
            mock_machine.return_value = "i686"
            assert get_arch_name() == "x86"
            get_arch_name.cache_clear()  # type: ignore[attr-defined]

            mock_machine.return_value = "i586"
            assert get_arch_name() == "x86"

    def test_get_arch_name_passthrough(self) -> None:
        """Test get_arch_name passes through unknown architectures."""
        with patch("platform.machine") as mock_machine:
            mock_machine.return_value = "unknown_arch"
            assert get_arch_name() == "unknown_arch"

    def test_get_arch_name_exception(self) -> None:
        """Test get_arch_name raises PlatformError on exception."""
        with patch("platform.machine", side_effect=RuntimeError("Test error")):
            with pytest.raises(PlatformError) as exc_info:
                get_arch_name()

            assert exc_info.value.code == "PLATFORM_ARCH_DETECTION_FAILED"
            assert exc_info.value.message == "Failed to detect architecture"

    @patch("provide.foundation.platform.detection.get_arch_name")
    @patch("provide.foundation.platform.detection.get_os_name")
    def test_get_platform_string(self, mock_os: Any, mock_arch: Any) -> None:
        """Test get_platform_string combines OS and arch."""
        mock_os.return_value = "darwin"
        mock_arch.return_value = "arm64"

        result = get_platform_string()
        assert result == "darwin_arm64"

    def test_get_os_version_darwin(self) -> None:
        """Test get_os_version for Darwin/macOS."""
        with (
            patch("platform.system", return_value="Darwin"),
            patch("platform.mac_ver", return_value=("14.2.1", "", "")),
        ):
            version = get_os_version()
            assert version == "14.2.1"

    def test_get_os_version_linux(self) -> None:
        """Test get_os_version for Linux."""
        with (
            patch("platform.system", return_value="Linux"),
            patch("platform.release", return_value="5.15.0-91-generic"),
        ):
            version = get_os_version()
            assert version == "5.15"

    def test_get_os_version_windows(self) -> None:
        """Test get_os_version for Windows."""
        with (
            patch("platform.system", return_value="Windows"),
            patch("platform.version", return_value="10.0.19045"),
        ):
            version = get_os_version()
            assert version == "10.0.19045"

    def test_get_os_version_fallback(self) -> None:
        """Test get_os_version fallback to platform.release."""
        with (
            patch("platform.system", return_value="UnknownOS"),
            patch("platform.release", return_value="1.0.0"),
        ):
            version = get_os_version()
            assert version == "1.0.0"

    def test_get_os_version_none(self) -> None:
        """Test get_os_version returns None when unavailable."""
        with (
            patch("platform.system", return_value="UnknownOS"),
            patch("platform.release", return_value=""),
        ):
            version = get_os_version()
            assert version is None

    def test_get_os_version_exception(self) -> None:
        """Test get_os_version handles exceptions gracefully."""
        with patch("platform.system", side_effect=RuntimeError("Test error")):
            version = get_os_version()
            assert version is None

    def test_get_cpu_type_intel(self) -> None:
        """Test get_cpu_type for Intel processors."""
        with patch(
            "platform.processor",
            return_value="Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz",
        ):
            cpu_type = get_cpu_type()
            assert cpu_type == "Intel Core i7"

    def test_get_cpu_type_amd_ryzen(self) -> None:
        """Test get_cpu_type for AMD Ryzen processors."""
        with patch(
            "platform.processor",
            return_value="AMD Ryzen 7 3700X 8-Core Processor",
        ):
            cpu_type = get_cpu_type()
            assert cpu_type == "AMD Ryzen 7"

    def test_get_cpu_type_apple_silicon(self) -> None:
        """Test get_cpu_type for Apple Silicon."""
        with patch("platform.processor", return_value="Apple M2"):
            cpu_type = get_cpu_type()
            assert cpu_type == "Apple M2"

    def test_get_cpu_type_generic_intel(self) -> None:
        """Test get_cpu_type for generic Intel processor."""
        with patch("platform.processor", return_value="Intel Something"):
            cpu_type = get_cpu_type()
            assert cpu_type == "Intel"

    def test_get_cpu_type_generic_amd(self) -> None:
        """Test get_cpu_type for generic AMD processor."""
        with patch("platform.processor", return_value="AMD Something"):
            cpu_type = get_cpu_type()
            assert cpu_type == "AMD"

    def test_get_cpu_type_apple_fallback(self) -> None:
        """Test get_cpu_type for Apple processor without specific model."""
        with patch("platform.processor", return_value="Apple Something"):
            cpu_type = get_cpu_type()
            assert cpu_type == "Apple Silicon"

    def test_get_cpu_type_unknown(self) -> None:
        """Test get_cpu_type for unknown processor."""
        with patch("platform.processor", return_value="Unknown Processor Type"):
            cpu_type = get_cpu_type()
            assert cpu_type == "Unknown Processor Type"

    def test_get_cpu_type_none(self) -> None:
        """Test get_cpu_type returns None when unavailable."""
        with patch("platform.processor", return_value=""):
            cpu_type = get_cpu_type()
            assert cpu_type is None

    def test_get_cpu_type_exception(self) -> None:
        """Test get_cpu_type handles exceptions gracefully."""
        with patch("platform.processor", side_effect=RuntimeError("Test error")):
            cpu_type = get_cpu_type()
            assert cpu_type is None

    def test_normalize_platform_components_basic(self) -> None:
        """Test normalize_platform_components with basic inputs."""
        os_name, arch_name = normalize_platform_components("Darwin", "x86_64")
        assert os_name == "darwin"
        assert arch_name == "amd64"

    def test_normalize_platform_components_variations(self) -> None:
        """Test normalize_platform_components with OS/arch variations."""
        # Test macOS normalization
        os_name, arch_name = normalize_platform_components("macOS", "aarch64")
        assert os_name == "darwin"
        assert arch_name == "arm64"

        # Test Windows variations
        os_name, arch_name = normalize_platform_components("win32", "i686")
        assert os_name == "windows"
        assert arch_name == "x86"

    def test_normalize_platform_components_passthrough(self) -> None:
        """Test normalize_platform_components passes through unknown values."""
        os_name, arch_name = normalize_platform_components("unknown_os", "unknown_arch")
        assert os_name == "unknown_os"
        assert arch_name == "unknown_arch"

    def test_normalize_platform_components_case_insensitive(self) -> None:
        """Test normalize_platform_components is case-insensitive."""
        os_name, arch_name = normalize_platform_components("LINUX", "AMD64")
        assert os_name == "linux"
        assert arch_name == "amd64"


# 🧱🏗️🔚
