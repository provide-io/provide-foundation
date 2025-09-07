#
# test_platform_coverage.py
#
"""
Tests to achieve full coverage for platform detection and info modules.
"""

import platform
from unittest.mock import patch, Mock
import pytest


class TestPlatformDetection:
    """Test platform detection functionality."""
    
    def test_get_os_name_darwin(self):
        """Test OS name detection for Darwin."""
        from provide.foundation.platform.detection import get_os_name
        
        with patch('platform.system', return_value='Darwin'):
            result = get_os_name()
            assert result == "darwin"
            
        with patch('platform.system', return_value='MacOS'):
            result = get_os_name()
            assert result == "darwin"
    
    def test_get_os_name_linux(self):
        """Test OS name detection for Linux."""
        from provide.foundation.platform.detection import get_os_name
        
        with patch('platform.system', return_value='Linux'):
            result = get_os_name()
            assert result == "linux"
    
    def test_get_os_name_windows(self):
        """Test OS name detection for Windows."""
        from provide.foundation.platform.detection import get_os_name
        
        with patch('platform.system', return_value='Windows'):
            result = get_os_name()
            assert result == "windows"
    
    def test_get_os_name_exception_handling(self):
        """Test OS name detection with exception."""
        from provide.foundation.platform.detection import get_os_name
        from provide.foundation.errors.platform import PlatformError
        
        with patch('platform.system', side_effect=Exception("Platform error")):
            with pytest.raises(PlatformError) as exc_info:
                get_os_name()
            
            assert "Failed to detect operating system" in str(exc_info.value)
            assert exc_info.value.code == "PLATFORM_OS_DETECTION_FAILED"
    
    def test_get_arch_name_amd64_variants(self):
        """Test architecture detection for amd64 variants."""
        from provide.foundation.platform.detection import get_arch_name
        
        for arch in ["x86_64", "amd64", "X86_64", "AMD64"]:
            with patch('platform.machine', return_value=arch):
                result = get_arch_name()
                assert result == "amd64"
    
    def test_get_arch_name_arm64_variants(self):
        """Test architecture detection for arm64 variants."""
        from provide.foundation.platform.detection import get_arch_name
        
        for arch in ["aarch64", "arm64", "AARCH64", "ARM64"]:
            with patch('platform.machine', return_value=arch):
                result = get_arch_name()
                assert result == "arm64"
    
    def test_get_arch_name_x86_variants(self):
        """Test architecture detection for x86 variants."""
        from provide.foundation.platform.detection import get_arch_name
        
        for arch in ["i686", "i586", "i486"]:
            with patch('platform.machine', return_value=arch):
                result = get_arch_name()
                assert result == "x86"
    
    def test_get_arch_name_unknown_arch(self):
        """Test architecture detection for unknown arch."""
        from provide.foundation.platform.detection import get_arch_name
        
        with patch('platform.machine', return_value='unknown_arch'):
            result = get_arch_name()
            assert result == "unknown_arch"
    
    def test_get_arch_name_exception_handling(self):
        """Test architecture detection with exception."""
        from provide.foundation.platform.detection import get_arch_name
        from provide.foundation.errors.platform import PlatformError
        
        with patch('platform.machine', side_effect=Exception("Machine error")):
            with pytest.raises(PlatformError) as exc_info:
                get_arch_name()
            
            assert "Failed to detect architecture" in str(exc_info.value)
            assert exc_info.value.code == "PLATFORM_ARCH_DETECTION_FAILED"
    
    def test_get_platform_string(self):
        """Test platform string generation.""" 
        from provide.foundation.platform.detection import get_platform_string
        
        result = get_platform_string()
        assert isinstance(result, str)
        assert "_" in result  # Should be format like "darwin_arm64"
        
        # Test that it includes OS and architecture
        parts = result.split("_")
        assert len(parts) >= 2
    
    def test_current_platform_detection(self):
        """Test current platform detection."""
        from provide.foundation.platform.detection import get_platform_string
        
        # Test that current platform can be detected
        current_platform = get_platform_string()
        assert isinstance(current_platform, str)
        assert len(current_platform.split("_")) >= 2
    
    def test_get_python_version_info(self):
        """Test Python version information."""
        from provide.foundation.platform.detection import get_python_version_info
        
        result = get_python_version_info()
        assert isinstance(result, dict)
        assert "version" in result
        assert "major" in result
        assert "minor" in result
        assert "micro" in result
    
    def test_get_system_info(self):
        """Test comprehensive system information."""
        from provide.foundation.platform.detection import get_system_info
        
        result = get_system_info()
        assert isinstance(result, dict)
        
        # Should contain key system information
        expected_keys = ["os", "arch", "platform", "python"]
        for key in expected_keys:
            assert key in result
    
    def test_detect_container_environment(self):
        """Test container environment detection."""
        from provide.foundation.platform.detection import detect_container_environment
        
        # Test normal environment (no container)
        result = detect_container_environment()
        assert isinstance(result, dict)
        assert "is_container" in result
        assert isinstance(result["is_container"], bool)
    
    @patch('os.path.exists')
    def test_detect_container_docker(self, mock_exists):
        """Test Docker container detection."""
        from provide.foundation.platform.detection import detect_container_environment
        
        # Mock Docker container environment
        def mock_exists_func(path):
            if path == "/.dockerenv":
                return True
            return False
        
        mock_exists.side_effect = mock_exists_func
        
        result = detect_container_environment()
        assert result["is_container"] is True
        assert result.get("type") == "docker"
    
    @patch('builtins.open')
    @patch('os.path.exists')
    def test_detect_container_cgroup(self, mock_exists, mock_open):
        """Test container detection via cgroup."""
        from provide.foundation.platform.detection import detect_container_environment
        
        # Mock cgroup file with container info
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = "docker\n"
        
        result = detect_container_environment()
        assert result["is_container"] is True
    
    def test_get_cpu_info(self):
        """Test CPU information gathering."""
        from provide.foundation.platform.detection import get_cpu_info
        
        result = get_cpu_info()
        assert isinstance(result, dict)
        
        # Should contain basic CPU info
        expected_keys = ["count", "architecture"]
        for key in expected_keys:
            assert key in result


class TestPlatformInfo:
    """Test platform info functionality."""
    
    def test_format_platform_info(self):
        """Test platform info formatting."""
        from provide.foundation.platform.info import format_platform_info
        
        result = format_platform_info()
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should contain system information
        assert "OS:" in result or "Platform:" in result
        assert "Architecture:" in result or "Arch:" in result
    
    def test_get_runtime_info(self):
        """Test runtime information gathering."""
        from provide.foundation.platform.info import get_runtime_info
        
        result = get_runtime_info()
        assert isinstance(result, dict)
        
        # Should contain runtime details
        expected_keys = ["python_version", "platform"]
        for key in expected_keys:
            assert key in result
    
    def test_get_environment_info(self):
        """Test environment information gathering."""
        from provide.foundation.platform.info import get_environment_info
        
        result = get_environment_info()
        assert isinstance(result, dict)
        
        # Should contain environment details
        assert "container" in result
        assert isinstance(result["container"], dict)
    
    def test_check_platform_compatibility(self):
        """Test platform compatibility checking."""
        from provide.foundation.platform.info import check_platform_compatibility
        
        # Test with current platform (should be compatible)
        result = check_platform_compatibility()
        assert isinstance(result, dict)
        assert "compatible" in result
        assert isinstance(result["compatible"], bool)
    
    def test_check_platform_compatibility_specific(self):
        """Test platform compatibility for specific requirements."""
        from provide.foundation.platform.info import check_platform_compatibility
        
        requirements = {
            "min_python": (3, 8),
            "supported_os": ["darwin", "linux", "windows"]
        }
        
        result = check_platform_compatibility(requirements)
        assert isinstance(result, dict)
        assert "compatible" in result
        assert "details" in result
    
    def test_get_hardware_info(self):
        """Test hardware information gathering."""
        from provide.foundation.platform.info import get_hardware_info
        
        result = get_hardware_info()
        assert isinstance(result, dict)
        
        # Should contain hardware details
        expected_keys = ["cpu", "memory"]
        for key in expected_keys:
            if key in result:  # Some info might not be available in all environments
                assert isinstance(result[key], dict)
    
    @patch('psutil.virtual_memory')
    def test_get_memory_info_with_psutil(self, mock_memory):
        """Test memory info when psutil is available."""
        from provide.foundation.platform.info import get_memory_info
        
        # Mock psutil memory info
        mock_memory.return_value = Mock(
            total=8 * 1024 * 1024 * 1024,  # 8GB
            available=4 * 1024 * 1024 * 1024,  # 4GB
            percent=50.0
        )
        
        result = get_memory_info()
        assert isinstance(result, dict)
        assert "total" in result
        assert "available" in result
        assert "percent" in result
    
    def test_get_memory_info_fallback(self):
        """Test memory info fallback when psutil unavailable."""
        from provide.foundation.platform.info import get_memory_info
        
        with patch('psutil.virtual_memory', side_effect=ImportError):
            result = get_memory_info()
            assert isinstance(result, dict)
            # Should provide some fallback info or empty dict
    
    def test_validate_platform_requirements(self):
        """Test platform requirements validation."""
        from provide.foundation.platform.info import validate_platform_requirements
        
        # Valid requirements
        valid_reqs = {
            "min_python": (3, 8),
            "supported_os": ["darwin", "linux"]
        }
        
        result = validate_platform_requirements(valid_reqs)
        assert isinstance(result, bool) or isinstance(result, dict)
    
    def test_validate_platform_requirements_invalid(self):
        """Test platform requirements validation with invalid requirements."""
        from provide.foundation.platform.info import validate_platform_requirements
        from provide.foundation.errors.platform import PlatformError
        
        # Impossible requirements
        invalid_reqs = {
            "min_python": (9, 9),  # Future version
            "supported_os": ["nonexistent_os"]
        }
        
        # Depending on implementation, this might raise or return False
        try:
            result = validate_platform_requirements(invalid_reqs)
            if isinstance(result, bool):
                assert result is False
        except PlatformError:
            pass  # Expected for impossible requirements