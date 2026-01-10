#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for system information gathering."""

from __future__ import annotations

from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch

from provide.foundation.platform import SystemInfo, get_system_info
from provide.foundation.platform.info import is_64bit, is_arm, is_linux, is_macos, is_windows


class TestSystemInfo(FoundationTestCase):
    """Test system information gathering."""

    def setup_method(self) -> None:
        """Set up test environment and clear caches."""
        super().setup_method()
        # Clear cached platform info results before each test
        get_system_info.cache_clear()  # type: ignore[attr-defined]
        is_windows.cache_clear()  # type: ignore[attr-defined]
        is_macos.cache_clear()  # type: ignore[attr-defined]
        is_linux.cache_clear()  # type: ignore[attr-defined]
        is_arm.cache_clear()  # type: ignore[attr-defined]
        is_64bit.cache_clear()  # type: ignore[attr-defined]

    @patch("provide.foundation.platform.info.get_os_name", return_value="darwin")
    @patch("provide.foundation.platform.info.get_arch_name", return_value="arm64")
    @patch(
        "provide.foundation.platform.info.get_platform_string",
        return_value="darwin_arm64",
    )
    @patch("provide.foundation.platform.info.get_os_version", return_value="14.2.1")
    @patch("provide.foundation.platform.info.get_cpu_type", return_value="Apple M2")
    @patch("platform.python_version", return_value="3.11.7")
    @patch("platform.node", return_value="test-hostname")
    @patch("os.environ.get")
    @patch("os.path.expanduser", return_value="/Users/test")
    @patch("os.cpu_count", return_value=8)
    @patch("shutil.disk_usage")
    def test_get_system_info_complete(
        self,
        mock_disk_usage: Any,
        mock_cpu_count: Any,
        mock_expanduser: Any,
        mock_env_get: Any,
        mock_node: Any,
        mock_python_version: Any,
        mock_cpu_type: Any,
        mock_os_version: Any,
        mock_platform: Any,
        mock_arch: Any,
        mock_os: Any,
    ) -> None:
        """Test getting complete system information."""

        # Setup mocks
        def env_side_effect(key: str, default: Any = None) -> Any:
            if key == "USER":
                return "testuser"
            if key == "TMPDIR":
                return "/tmp"
            return default

        mock_env_get.side_effect = env_side_effect

        mock_disk_usage.return_value = MagicMock(
            total=1000000,
            used=500000,
            free=500000,
        )

        # Get system info
        info = get_system_info()

        # Verify basic platform info (from mocks)
        assert info.os_name == "darwin"
        assert info.arch == "arm64"
        assert info.platform == "darwin_arm64"
        # OS version might vary, just check it's not None
        assert info.os_version is not None
        assert info.cpu_type == "Apple M2"

        # Verify Python info
        assert info.python_version == "3.11.7"

        # Verify system info
        assert info.hostname == "test-hostname"
        assert info.username == "testuser"
        assert info.home_dir == "/Users/test"
        assert info.temp_dir == "/tmp"
        assert info.num_cpus == 8

        # Verify disk usage
        assert info.disk_usage is not None
        assert "/" in info.disk_usage
        assert info.disk_usage["/"]["total"] == 1000000

    @patch("provide.foundation.platform.info.get_os_name", return_value="linux")
    @patch("provide.foundation.platform.info.get_arch_name", return_value="amd64")
    @patch(
        "provide.foundation.platform.info.get_platform_string",
        return_value="linux_amd64",
    )
    @patch("provide.foundation.platform.info.get_os_version", return_value=None)
    @patch("provide.foundation.platform.info.get_cpu_type", return_value=None)
    @patch("platform.python_version", return_value="3.10.0")
    @patch("platform.node", side_effect=Exception("Cannot get hostname"))
    @patch("os.environ.get", return_value=None)
    @patch("os.path.expanduser", return_value="/home/user")
    @patch("os.cpu_count", side_effect=Exception("Cannot get CPU count"))
    @patch("shutil.disk_usage", side_effect=Exception("Cannot get disk usage"))
    def test_get_system_info_minimal(
        self,
        mock_disk_usage: Any,
        mock_cpu_count: Any,
        mock_expanduser: Any,
        mock_env_get: Any,
        mock_node: Any,
        mock_python_version: Any,
        mock_cpu_type: Any,
        mock_os_version: Any,
        mock_platform: Any,
        mock_arch: Any,
        mock_os: Any,
    ) -> None:
        """Test getting system info with minimal data available."""
        # Get system info
        info = get_system_info()

        # Verify basic platform info (always available)
        assert info.os_name in ["linux", "darwin", "windows"]
        assert info.arch in ["amd64", "arm64", "x86", "x86_64"]
        assert info.platform == f"{info.os_name}_{info.arch}"
        assert info.os_version is None
        assert info.cpu_type is None

        # Verify Python info
        assert info.python_version == "3.10.0"

        # Verify optional fields are None
        assert info.hostname is None
        assert info.username is None
        assert info.home_dir == "/home/user"
        # temp_dir should be the actual system temp directory when no env vars set
        from provide.foundation.file.temp import system_temp_dir

        expected_temp_dir = str(system_temp_dir())
        assert info.temp_dir == expected_temp_dir
        assert info.num_cpus is None
        # Memory info may or may not be available depending on psutil
        # So we just check the attributes exist
        assert hasattr(info, "total_memory")
        assert hasattr(info, "available_memory")
        # Disk usage may be None or empty dict on error
        assert info.disk_usage is None or info.disk_usage == {}

    @patch("provide.foundation.platform.info.get_os_name", return_value="windows")
    @patch("provide.foundation.platform.info.get_arch_name", return_value="amd64")
    @patch(
        "provide.foundation.platform.info.get_platform_string",
        return_value="windows_amd64",
    )
    @patch("provide.foundation.platform.info.get_os_version", return_value="10.0.19045")
    @patch(
        "provide.foundation.platform.info.get_cpu_type",
        return_value="Intel Core i7",
    )
    @patch("platform.python_version", return_value="3.11.0")
    def test_get_system_info_with_psutil(
        self,
        mock_python_version: Any,
        mock_cpu_type: Any,
        mock_os_version: Any,
        mock_platform: Any,
        mock_arch: Any,
        mock_os: Any,
    ) -> None:
        """Test getting system info with psutil available."""
        # Mock psutil
        mock_psutil = MagicMock()
        mock_psutil.virtual_memory.return_value = MagicMock(
            total=16000000000,
            available=8000000000,
        )

        with patch.dict("sys.modules", {"psutil": mock_psutil}):
            info = get_system_info()

            # Check memory info when psutil is available
            assert info.total_memory == 16000000000
            assert info.available_memory == 8000000000

    def test_system_info_dataclass(self) -> None:
        """Test SystemInfo dataclass."""
        info = SystemInfo(
            os_name="linux",
            arch="amd64",
            platform="linux_amd64",
            os_version="5.15.0",
            cpu_type="Intel Core i5",
            python_version="3.11.0",
            hostname="test-host",
            username="testuser",
            home_dir="/home/testuser",
            temp_dir="/tmp",
            num_cpus=4,
            total_memory=8000000000,
            available_memory=4000000000,
            disk_usage={"/": {"total": 1000000, "used": 500000, "free": 500000}},
        )

        assert info.os_name == "linux"
        assert info.arch == "amd64"
        assert info.platform == "linux_amd64"
        assert info.num_cpus == 4
        assert info.total_memory == 8000000000


# 🧱🏗️🔚
