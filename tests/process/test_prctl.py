#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import sys

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.errors.platform import PlatformError


class TestPrctl(FoundationTestCase):
    """Test prctl functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_has_prctl_returns_bool(self) -> None:
        """Test has_prctl returns boolean."""
        from provide.foundation.process import has_prctl

        result = has_prctl()
        assert isinstance(result, bool)

    def test_is_linux_returns_bool(self) -> None:
        """Test is_linux returns boolean."""
        from provide.foundation.process import is_linux

        result = is_linux()
        assert isinstance(result, bool)

    def test_has_prctl_false_on_non_linux(self) -> None:
        """Test has_prctl returns False on non-Linux systems."""
        with patch("provide.foundation.process.prctl._IS_LINUX", False):
            from provide.foundation.process.prctl import has_prctl

            result = has_prctl()
            assert result is False

    def test_set_death_signal_raises_on_non_linux(self) -> None:
        """Test set_death_signal raises PlatformError on non-Linux."""
        with patch("provide.foundation.process.prctl._IS_LINUX", False):
            from provide.foundation.process import set_death_signal

            with pytest.raises(PlatformError) as exc_info:
                set_death_signal(15)
            assert "only available on Linux" in str(exc_info.value)

    def test_set_death_signal_raises_without_prctl(self) -> None:
        """Test set_death_signal raises PlatformError when prctl not installed."""
        with patch("provide.foundation.process.prctl._IS_LINUX", True):
            with patch("provide.foundation.process.prctl._HAS_PRCTL", False):
                from provide.foundation.process import set_death_signal

                with pytest.raises(PlatformError) as exc_info:
                    set_death_signal(15)
                assert "not installed" in str(exc_info.value)

    def test_set_dumpable_raises_on_non_linux(self) -> None:
        """Test set_dumpable raises PlatformError on non-Linux."""
        with patch("provide.foundation.process.prctl._IS_LINUX", False):
            from provide.foundation.process import set_dumpable

            with pytest.raises(PlatformError):
                set_dumpable(True)

    def test_set_name_raises_on_non_linux(self) -> None:
        """Test set_name raises PlatformError on non-Linux."""
        with patch("provide.foundation.process.prctl._IS_LINUX", False):
            from provide.foundation.process import set_name

            with pytest.raises(PlatformError):
                set_name("test")

    def test_get_name_raises_on_non_linux(self) -> None:
        """Test get_name raises PlatformError on non-Linux."""
        with patch("provide.foundation.process.prctl._IS_LINUX", False):
            from provide.foundation.process import get_name

            with pytest.raises(PlatformError):
                get_name()

    def test_set_no_new_privs_raises_on_non_linux(self) -> None:
        """Test set_no_new_privs raises PlatformError on non-Linux."""
        with patch("provide.foundation.process.prctl._IS_LINUX", False):
            from provide.foundation.process import set_no_new_privs

            with pytest.raises(PlatformError):
                set_no_new_privs(True)

    @pytest.mark.skipif(
        not sys.platform.startswith("linux"),
        reason="prctl only available on Linux",
    )
    def test_set_death_signal_with_prctl_available(self) -> None:
        """Test set_death_signal when prctl is available (Linux only)."""
        from provide.foundation.process import has_prctl

        if not has_prctl():
            pytest.skip("python-prctl not installed")

        import signal

        from provide.foundation.process import set_death_signal

        result = set_death_signal(signal.SIGTERM)
        assert isinstance(result, bool)

    @pytest.mark.skipif(
        not sys.platform.startswith("linux"),
        reason="prctl only available on Linux",
    )
    def test_set_dumpable_with_prctl_available(self) -> None:
        """Test set_dumpable when prctl is available (Linux only)."""
        from provide.foundation.process import has_prctl

        if not has_prctl():
            pytest.skip("python-prctl not installed")

        from provide.foundation.process import set_dumpable

        result = set_dumpable(True)
        assert isinstance(result, bool)

    @pytest.mark.skipif(
        not sys.platform.startswith("linux"),
        reason="prctl only available on Linux",
    )
    def test_set_name_with_prctl_available(self) -> None:
        """Test set_name when prctl is available (Linux only)."""
        from provide.foundation.process import has_prctl

        if not has_prctl():
            pytest.skip("python-prctl not installed")

        from provide.foundation.process import set_name

        result = set_name("test-proc")
        assert isinstance(result, bool)

    @pytest.mark.skipif(
        not sys.platform.startswith("linux"),
        reason="prctl only available on Linux",
    )
    def test_get_name_with_prctl_available(self) -> None:
        """Test get_name when prctl is available (Linux only)."""
        from provide.foundation.process import has_prctl

        if not has_prctl():
            pytest.skip("python-prctl not installed")

        from provide.foundation.process import get_name

        name = get_name()
        assert name is None or isinstance(name, str)

    # Skipping detailed exception/mock tests for optional Linux modules on non-Linux systems


# 🧱🏗️🔚
