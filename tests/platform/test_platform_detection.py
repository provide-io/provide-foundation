"""Tests for platform detection functionality."""

import platform
import pytest
from unittest.mock import patch, MagicMock

from provide.foundation.platform import (
    get_os_name,
    get_arch_name,
    get_platform_string,
    get_os_version,
    get_cpu_type,
    normalize_platform_components,
)
from provide.foundation.platform.detection import PlatformError


class TestPlatformDetection:
    """Test platform detection functions."""
    
    def test_get_os_name_darwin(self):
        """Test OS name detection on macOS."""
        with patch("platform.system", return_value="Darwin"):
            assert get_os_name() == "darwin"
    
    def test_get_os_name_linux(self):
        """Test OS name detection on Linux."""
        with patch("platform.system", return_value="Linux"):
            assert get_os_name() == "linux"
    
    def test_get_os_name_windows(self):
        """Test OS name detection on Windows."""
        with patch("platform.system", return_value="Windows"):
            assert get_os_name() == "windows"
    
    def test_get_os_name_error(self):
        """Test OS name detection error handling."""
        with patch("platform.system", side_effect=Exception("Test error")):
            with pytest.raises(PlatformError, match="Failed to detect operating system"):
                get_os_name()
    
    def test_get_arch_name_amd64(self):
        """Test architecture detection for x86_64."""
        with patch("platform.machine", return_value="x86_64"):
            assert get_arch_name() == "amd64"
    
    def test_get_arch_name_arm64(self):
        """Test architecture detection for ARM64."""
        with patch("platform.machine", return_value="aarch64"):
            assert get_arch_name() == "arm64"
        
        with patch("platform.machine", return_value="arm64"):
            assert get_arch_name() == "arm64"
    
    def test_get_arch_name_x86(self):
        """Test architecture detection for 32-bit x86."""
        with patch("platform.machine", return_value="i686"):
            assert get_arch_name() == "x86"
    
    def test_get_arch_name_unknown(self):
        """Test architecture detection for unknown arch."""
        with patch("platform.machine", return_value="riscv64"):
            assert get_arch_name() == "riscv64"
    
    def test_get_arch_name_error(self):
        """Test architecture detection error handling."""
        with patch("platform.machine", side_effect=Exception("Test error")):
            with pytest.raises(PlatformError, match="Failed to detect architecture"):
                get_arch_name()
    
    def test_get_platform_string(self):
        """Test platform string generation."""
        with patch("platform.system", return_value="Darwin"):
            with patch("platform.machine", return_value="arm64"):
                assert get_platform_string() == "darwin_arm64"
        
        with patch("platform.system", return_value="Linux"):
            with patch("platform.machine", return_value="x86_64"):
                assert get_platform_string() == "linux_amd64"
    
    def test_get_os_version_macos(self):
        """Test OS version detection on macOS."""
        with patch("platform.system", return_value="Darwin"):
            with patch("platform.mac_ver", return_value=("14.2.1", "", "")):
                assert get_os_version() == "14.2.1"
    
    def test_get_os_version_linux(self):
        """Test OS version detection on Linux."""
        with patch("platform.system", return_value="Linux"):
            with patch("platform.release", return_value="5.15.0-91-generic"):
                assert get_os_version() == "5.15"
    
    def test_get_os_version_windows(self):
        """Test OS version detection on Windows."""
        with patch("platform.system", return_value="Windows"):
            with patch("platform.version", return_value="10.0.19045"):
                assert get_os_version() == "10.0.19045"
    
    def test_get_os_version_fallback(self):
        """Test OS version fallback to release."""
        with patch("platform.system", return_value="Unknown"):
            with patch("platform.release", return_value="1.2.3"):
                assert get_os_version() == "1.2.3"
    
    def test_get_os_version_none(self):
        """Test OS version returns None on error."""
        with patch("platform.system", side_effect=Exception("Test error")):
            assert get_os_version() is None
    
    def test_get_cpu_type_intel(self):
        """Test CPU type detection for Intel processors."""
        with patch("platform.processor", return_value="Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz"):
            assert get_cpu_type() == "Intel Core i7"
        
        with patch("platform.processor", return_value="Intel Xeon"):
            assert get_cpu_type() == "Intel"
    
    def test_get_cpu_type_amd(self):
        """Test CPU type detection for AMD processors."""
        with patch("platform.processor", return_value="AMD Ryzen 9 5900X"):
            assert get_cpu_type() == "AMD Ryzen 9"
        
        with patch("platform.processor", return_value="AMD EPYC"):
            assert get_cpu_type() == "AMD"
    
    def test_get_cpu_type_apple(self):
        """Test CPU type detection for Apple Silicon."""
        with patch("platform.processor", return_value="Apple M1 Max"):
            assert get_cpu_type() == "Apple M1"
        
        with patch("platform.processor", return_value="Apple M2"):
            assert get_cpu_type() == "Apple M2"
    
    def test_get_cpu_type_unknown(self):
        """Test CPU type for unknown processor."""
        with patch("platform.processor", return_value="Unknown Processor"):
            assert get_cpu_type() == "Unknown Processor"
    
    def test_get_cpu_type_none(self):
        """Test CPU type returns None on error."""
        with patch("platform.processor", side_effect=Exception("Test error")):
            assert get_cpu_type() is None
    
    def test_normalize_platform_components(self):
        """Test platform component normalization."""
        # OS normalization
        assert normalize_platform_components("Darwin", "x86_64") == ("darwin", "amd64")
        assert normalize_platform_components("macos", "arm64") == ("darwin", "arm64")
        assert normalize_platform_components("Linux", "aarch64") == ("linux", "arm64")
        assert normalize_platform_components("Windows", "x86_64") == ("windows", "amd64")
        assert normalize_platform_components("win32", "i686") == ("windows", "x86")
        
        # Unknown values pass through lowercased
        assert normalize_platform_components("FreeBSD", "riscv64") == ("freebsd", "riscv64")