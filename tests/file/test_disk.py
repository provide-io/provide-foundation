#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for disk space and filesystem utilities."""

from __future__ import annotations

from pathlib import Path

from provide.testkit.mocking import patch
import pytest

from provide.foundation.file.disk import (
    check_disk_space,
    format_bytes,
    get_available_space,
    get_disk_usage,
)


class TestGetAvailableSpace:
    """Tests for get_available_space function."""

    def test_get_available_space_existing_path(self, tmp_path: Path) -> None:
        """Should return available space for existing path."""
        space = get_available_space(tmp_path)

        # Should return a positive integer
        assert space is not None
        assert isinstance(space, int)
        assert space > 0

    def test_get_available_space_nonexistent_path(self, tmp_path: Path) -> None:
        """Should use parent directory for non-existent path."""
        # Use a single-level nonexistent path (parent exists)
        nonexistent = tmp_path / "nonexistent"
        space = get_available_space(nonexistent)

        # Should still return space (using parent which exists)
        assert space is not None
        assert space > 0

    def test_get_available_space_home_directory(self) -> None:
        """Should work with home directory."""
        space = get_available_space(Path.home())

        assert space is not None
        assert space > 0

    @patch("os.statvfs")
    def test_get_available_space_handles_os_error(self, mock_statvfs, tmp_path: Path) -> None:
        """Should return None when os.statvfs raises OSError."""
        mock_statvfs.side_effect = OSError("Permission denied")

        space = get_available_space(tmp_path)

        assert space is None

    @patch("os.statvfs")
    def test_get_available_space_handles_attribute_error(self, mock_statvfs, tmp_path: Path) -> None:
        """Should return None when statvfs is not available (Windows)."""
        mock_statvfs.side_effect = AttributeError("statvfs not available")

        space = get_available_space(tmp_path)

        assert space is None


class TestCheckDiskSpace:
    """Tests for check_disk_space function."""

    def test_check_disk_space_sufficient(self, tmp_path: Path) -> None:
        """Should return True when sufficient space available."""
        # Request 1KB (should always be available)
        result = check_disk_space(tmp_path, 1024, raise_on_insufficient=False)

        assert result is True

    def test_check_disk_space_insufficient_no_raise(self, tmp_path: Path) -> None:
        """Should return False when insufficient space and raise_on_insufficient=False."""
        # Request an impossibly large amount
        huge_requirement = 10**18  # 1 exabyte

        result = check_disk_space(tmp_path, huge_requirement, raise_on_insufficient=False)

        assert result is False

    def test_check_disk_space_insufficient_raises(self, tmp_path: Path) -> None:
        """Should raise OSError when insufficient space and raise_on_insufficient=True."""
        # Request an impossibly large amount
        huge_requirement = 10**18  # 1 exabyte

        with pytest.raises(OSError, match="Insufficient disk space"):
            check_disk_space(tmp_path, huge_requirement, raise_on_insufficient=True)

    def test_check_disk_space_default_raises(self, tmp_path: Path) -> None:
        """Should raise by default when insufficient space."""
        huge_requirement = 10**18

        with pytest.raises(OSError, match="Insufficient disk space"):
            check_disk_space(tmp_path, huge_requirement)  # Default raise_on_insufficient=True

    def test_check_disk_space_nonexistent_path(self, tmp_path: Path) -> None:
        """Should use parent directory for non-existent path."""
        nonexistent = tmp_path / "does" / "not" / "exist"

        result = check_disk_space(nonexistent, 1024, raise_on_insufficient=False)

        # Should succeed using parent
        assert result is True

    @patch("provide.foundation.file.disk.get_available_space")
    def test_check_disk_space_when_space_unknown(self, mock_get_space, tmp_path: Path) -> None:
        """Should return True (allow operation) when space cannot be determined."""
        mock_get_space.return_value = None

        result = check_disk_space(tmp_path, 1024, raise_on_insufficient=False)

        # Should allow operation to proceed
        assert result is True

    def test_check_disk_space_just_under_requirement(self, tmp_path: Path) -> None:
        """Should succeed when requirement is slightly under available."""
        # Get actual available space
        available = get_available_space(tmp_path)
        assert available is not None

        # Request 90% of what's available (should succeed)
        requirement = int(available * 0.9)
        result = check_disk_space(tmp_path, requirement, raise_on_insufficient=False)

        # Should succeed (available >= required)
        assert result is True

    def test_check_disk_space_one_byte_over(self, tmp_path: Path) -> None:
        """Should fail when requirement is one byte more than available."""
        with patch("provide.foundation.file.disk.get_available_space") as mock_get_space:
            mock_get_space.return_value = 1024

            result = check_disk_space(tmp_path, 1025, raise_on_insufficient=False)

            # Should fail
            assert result is False
            mock_get_space.assert_called_once_with(tmp_path)


class TestGetDiskUsage:
    """Tests for get_disk_usage function."""

    def test_get_disk_usage_existing_path(self, tmp_path: Path) -> None:
        """Should return disk usage for existing path."""
        usage = get_disk_usage(tmp_path)

        assert usage is not None
        total, used, free = usage

        # All values should be positive
        assert total > 0
        assert used >= 0
        assert free > 0

        # Total should be >= used + free (may have reserved space)
        assert total >= used

    def test_get_disk_usage_nonexistent_path(self, tmp_path: Path) -> None:
        """Should use parent for non-existent path."""
        nonexistent = tmp_path / "nonexistent"
        usage = get_disk_usage(nonexistent)

        assert usage is not None
        total, _used, _free = usage
        assert total > 0

    def test_get_disk_usage_home_directory(self) -> None:
        """Should work with home directory."""
        usage = get_disk_usage(Path.home())

        assert usage is not None
        total, used, free = usage
        assert total > 0
        assert used > 0
        assert free > 0

    @patch("os.statvfs")
    def test_get_disk_usage_handles_os_error(self, mock_statvfs, tmp_path: Path) -> None:
        """Should return None when os.statvfs raises OSError."""
        mock_statvfs.side_effect = OSError("Permission denied")

        usage = get_disk_usage(tmp_path)

        assert usage is None

    @patch("os.statvfs")
    def test_get_disk_usage_handles_attribute_error(self, mock_statvfs, tmp_path: Path) -> None:
        """Should return None when statvfs not available."""
        mock_statvfs.side_effect = AttributeError("statvfs not available")

        usage = get_disk_usage(tmp_path)

        assert usage is None


class TestFormatBytes:
    """Tests for format_bytes function."""

    def test_format_bytes_bytes(self) -> None:
        """Should format bytes correctly."""
        assert format_bytes(0) == "0.00 B"
        assert format_bytes(500) == "500.00 B"
        assert format_bytes(1023) == "1023.00 B"

    def test_format_bytes_kilobytes(self) -> None:
        """Should format kilobytes correctly."""
        assert format_bytes(1024) == "1.00 KB"
        assert format_bytes(1536) == "1.50 KB"
        assert format_bytes(2048) == "2.00 KB"

    def test_format_bytes_megabytes(self) -> None:
        """Should format megabytes correctly."""
        assert format_bytes(1024**2) == "1.00 MB"
        assert format_bytes(int(1.5 * 1024**2)) == "1.50 MB"
        assert format_bytes(100 * 1024**2) == "100.00 MB"

    def test_format_bytes_gigabytes(self) -> None:
        """Should format gigabytes correctly."""
        assert format_bytes(1024**3) == "1.00 GB"
        assert format_bytes(int(2.5 * 1024**3)) == "2.50 GB"
        assert format_bytes(1000 * 1024**3) == "1000.00 GB"

    def test_format_bytes_terabytes(self) -> None:
        """Should format terabytes correctly."""
        assert format_bytes(1024**4) == "1.00 TB"
        assert format_bytes(int(5.25 * 1024**4)) == "5.25 TB"

    def test_format_bytes_petabytes(self) -> None:
        """Should format petabytes correctly."""
        assert format_bytes(1024**5) == "1.00 PB"
        assert format_bytes(10 * 1024**5) == "10.00 PB"

    def test_format_bytes_very_large(self) -> None:
        """Should handle very large values."""
        # Beyond petabytes should still show as PB
        assert "PB" in format_bytes(1024**6)


class TestDiskUtilitiesIntegration:
    """Integration tests combining multiple disk utilities."""

    def test_check_and_get_workflow(self, tmp_path: Path) -> None:
        """Test typical workflow: get space, then check requirement."""
        # Get available space
        available = get_available_space(tmp_path)
        assert available is not None

        # Check for reasonable requirement (10% of available)
        requirement = available // 10
        result = check_disk_space(tmp_path, requirement, raise_on_insufficient=False)
        assert result is True

        # Check for unreasonable requirement (200% of available)
        huge_requirement = available * 2
        result = check_disk_space(tmp_path, huge_requirement, raise_on_insufficient=False)
        assert result is False

    def test_usage_and_available_consistent(self, tmp_path: Path) -> None:
        """Test that usage and available space are consistent."""
        available = get_available_space(tmp_path)
        usage = get_disk_usage(tmp_path)

        if available is not None and usage is not None:
            _total, _used, free = usage

            # Available space should be close to free space
            # (May differ due to reserved space for root)
            # Allow 10% difference
            assert abs(available - free) / free < 0.1 or available <= free

    def test_format_available_space(self, tmp_path: Path) -> None:
        """Test formatting available space for display."""
        available = get_available_space(tmp_path)
        assert available is not None

        formatted = format_bytes(available)

        # Should contain a number and a unit
        assert any(unit in formatted for unit in ["B", "KB", "MB", "GB", "TB", "PB"])
        assert formatted.split()[0].replace(".", "").isdigit()


class TestDiskUtilitiesEdgeCases:
    """Tests for edge cases and error handling."""

    def test_check_disk_space_zero_requirement(self, tmp_path: Path) -> None:
        """Should succeed when requirement is zero."""
        result = check_disk_space(tmp_path, 0, raise_on_insufficient=False)
        assert result is True

    def test_check_disk_space_negative_requirement(self, tmp_path: Path) -> None:
        """Should succeed when requirement is negative (unusual but valid)."""
        result = check_disk_space(tmp_path, -1000, raise_on_insufficient=False)
        assert result is True

    def test_format_bytes_zero(self) -> None:
        """Should handle zero bytes."""
        assert format_bytes(0) == "0.00 B"

    def test_format_bytes_negative(self) -> None:
        """Should handle negative values (unusual but valid)."""
        result = format_bytes(-1024)
        # Should still format, showing negative
        assert "-" in result

    @patch("os.statvfs")
    def test_all_functions_graceful_failure(self, mock_statvfs, tmp_path: Path) -> None:
        """Test that all functions handle statvfs unavailability gracefully."""
        mock_statvfs.side_effect = AttributeError("Not available")

        # get_available_space should return None
        assert get_available_space(tmp_path) is None

        # check_disk_space should return True (allow operation)
        assert check_disk_space(tmp_path, 1024, raise_on_insufficient=False) is True

        # get_disk_usage should return None
        assert get_disk_usage(tmp_path) is None


# 🧱🏗️🔚
