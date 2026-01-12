#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch
import pytest


class TestCPUInfo(FoundationTestCase):
    """Test CPU information functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_has_cpuinfo_returns_bool(self) -> None:
        """Test has_cpuinfo returns boolean."""
        from provide.foundation.platform import has_cpuinfo

        result = has_cpuinfo()
        assert isinstance(result, bool)

    def test_get_cpu_info_returns_dict(self) -> None:
        """Test get_cpu_info returns dictionary."""
        from provide.foundation.platform import get_cpu_info

        info = get_cpu_info()
        assert isinstance(info, dict)
        # py-cpuinfo uses "brand_raw", fallback uses "brand"
        assert "brand" in info or "brand_raw" in info
        assert "arch" in info or "arch_string_raw" in info

    def test_get_cpu_info_with_cpuinfo_available(self) -> None:
        """Test get_cpu_info when py-cpuinfo is available."""
        from provide.foundation.platform import get_cpu_info, has_cpuinfo

        if not has_cpuinfo():
            pytest.skip("py-cpuinfo not available")

        info = get_cpu_info()
        assert isinstance(info, dict)
        # Should have detailed info from py-cpuinfo (uses brand_raw)
        brand = info.get("brand_raw") or info.get("brand")
        assert brand is not None

    def test_get_cpu_info_without_cpuinfo(self) -> None:
        """Test get_cpu_info falls back to platform module when py-cpuinfo unavailable."""
        with patch("provide.foundation.platform.cpu._HAS_CPUINFO", False):
            # Clear cache to force re-execution
            from provide.foundation.platform.cpu import get_cpu_info

            get_cpu_info.cache_clear()

            info = get_cpu_info()
            assert isinstance(info, dict)
            assert "brand" in info
            assert "arch" in info
            assert info["flags"] is None  # Fallback doesn't have flags

    def test_get_cpu_brand_returns_string(self) -> None:
        """Test get_cpu_brand returns string."""
        from provide.foundation.platform import get_cpu_brand

        brand = get_cpu_brand()
        assert isinstance(brand, str)
        assert len(brand) > 0

    def test_get_cpu_flags_returns_list(self) -> None:
        """Test get_cpu_flags returns list."""
        from provide.foundation.platform import get_cpu_flags

        flags = get_cpu_flags()
        assert isinstance(flags, list)

    def test_get_cpu_flags_with_cpuinfo_available(self) -> None:
        """Test get_cpu_flags when py-cpuinfo is available."""
        from provide.foundation.platform import get_cpu_flags, has_cpuinfo

        if not has_cpuinfo():
            pytest.skip("py-cpuinfo not available")

        flags = get_cpu_flags()
        assert isinstance(flags, list)
        # On some platforms (like ARM Mac), py-cpuinfo may not return flags
        # Just verify it's a list

    def test_get_cpu_flags_without_cpuinfo(self) -> None:
        """Test get_cpu_flags returns empty list when py-cpuinfo unavailable."""
        with patch("provide.foundation.platform.cpu._HAS_CPUINFO", False):
            from provide.foundation.platform.cpu import get_cpu_info

            get_cpu_info.cache_clear()

            from provide.foundation.platform import get_cpu_flags

            flags = get_cpu_flags()
            assert isinstance(flags, list)
            assert len(flags) == 0  # Fallback has no flags

    def test_has_cpu_flag_returns_bool(self) -> None:
        """Test has_cpu_flag returns boolean."""
        from provide.foundation.platform import has_cpu_flag

        result = has_cpu_flag("sse2")
        assert isinstance(result, bool)

    def test_has_cpu_flag_case_insensitive(self) -> None:
        """Test has_cpu_flag is case insensitive."""
        from provide.foundation.platform import has_cpu_flag, has_cpuinfo

        if not has_cpuinfo():
            pytest.skip("py-cpuinfo not available")

        # Assuming most modern systems have SSE2
        result_lower = has_cpu_flag("sse2")
        result_upper = has_cpu_flag("SSE2")
        result_mixed = has_cpu_flag("Sse2")

        assert result_lower == result_upper == result_mixed

    def test_get_cpu_count_returns_int_or_none(self) -> None:
        """Test get_cpu_count returns int or None."""
        from provide.foundation.platform import get_cpu_count

        count = get_cpu_count()
        assert count is None or isinstance(count, int)
        if count is not None:
            assert count > 0

    def test_get_cpu_info_caching(self) -> None:
        """Test that get_cpu_info is cached."""
        from provide.foundation.platform.cpu import get_cpu_info

        # Call twice
        info1 = get_cpu_info()
        info2 = get_cpu_info()

        # Should be the same object (cached)
        assert info1 is info2

    def test_get_cpu_info_handles_cpuinfo_exception(self) -> None:
        """Test get_cpu_info handles exceptions from py-cpuinfo gracefully."""
        with patch("provide.foundation.platform.cpu._HAS_CPUINFO", True):
            with patch("provide.foundation.platform.cpu.cpuinfo") as mock_cpuinfo:
                mock_cpuinfo.get_cpu_info = MagicMock(side_effect=RuntimeError("Test error"))

                from provide.foundation.platform.cpu import get_cpu_info

                get_cpu_info.cache_clear()

                info = get_cpu_info()
                # Should fall back to platform module
                assert isinstance(info, dict)
                assert info["flags"] is None  # Fallback doesn't have flags

    def test_get_cpu_count_with_none_value(self) -> None:
        """Test get_cpu_count handles None from get_cpu_info."""
        with patch("provide.foundation.platform.cpu.get_cpu_info") as mock_get_cpu_info:
            mock_get_cpu_info.return_value = {"count": None}

            from provide.foundation.platform import get_cpu_count

            result = get_cpu_count()
            assert result is None

    def test_get_cpu_count_with_string_value(self) -> None:
        """Test get_cpu_count converts string to int."""
        with patch("provide.foundation.platform.cpu.get_cpu_info") as mock_get_cpu_info:
            mock_get_cpu_info.return_value = {"count": "8"}

            from provide.foundation.platform import get_cpu_count

            result = get_cpu_count()
            assert result == 8
            assert isinstance(result, int)


# 🧱🏗️🔚
