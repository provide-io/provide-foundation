#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for file permissions utilities."""

from __future__ import annotations

from pathlib import Path

import pytest

from provide.foundation.file.permissions import (
    DEFAULT_DIR_PERMS,
    DEFAULT_EXECUTABLE_PERMS,
    DEFAULT_FILE_PERMS,
    ensure_secure_permissions,
    format_permissions,
    get_permissions,
    parse_permissions,
    set_file_permissions,
)


class TestParsePermissions:
    """Tests for parse_permissions function."""

    def test_parse_octal_with_0_prefix(self) -> None:
        """Should parse octal string with '0' prefix."""
        assert parse_permissions("0755") == 0o755

    def test_parse_octal_with_0o_prefix(self) -> None:
        """Should parse octal string with '0o' prefix."""
        assert parse_permissions("0o755") == 0o755

    def test_parse_octal_without_prefix(self) -> None:
        """Should parse octal string without prefix."""
        assert parse_permissions("755") == 0o755

    def test_parse_different_permissions(self) -> None:
        """Should parse various permission values correctly."""
        assert parse_permissions("644") == 0o644
        assert parse_permissions("777") == 0o777
        assert parse_permissions("600") == 0o600
        assert parse_permissions("400") == 0o400

    def test_parse_none_returns_default(self) -> None:
        """Should return default when None is provided."""
        assert parse_permissions(None) == DEFAULT_FILE_PERMS

    def test_parse_empty_string_returns_default(self) -> None:
        """Should return default when empty string is provided."""
        assert parse_permissions("") == DEFAULT_FILE_PERMS

    def test_parse_invalid_returns_default(self) -> None:
        """Should return default when invalid string is provided."""
        assert parse_permissions("invalid") == DEFAULT_FILE_PERMS
        assert parse_permissions("999") == DEFAULT_FILE_PERMS  # Invalid octal
        assert parse_permissions("abc") == DEFAULT_FILE_PERMS

    def test_parse_with_custom_default(self) -> None:
        """Should use custom default when provided."""
        assert parse_permissions(None, default=0o777) == 0o777
        assert parse_permissions("invalid", default=0o600) == 0o600

    def test_parse_with_whitespace(self) -> None:
        """Should handle strings with whitespace."""
        assert parse_permissions("  755  ") == 0o755
        assert parse_permissions(" 0o644 ") == 0o644


class TestFormatPermissions:
    """Tests for format_permissions function."""

    def test_format_basic_permissions(self) -> None:
        """Should format basic permission values."""
        assert format_permissions(0o755) == "0755"
        assert format_permissions(0o644) == "0644"
        assert format_permissions(0o777) == "0777"

    def test_format_from_decimal(self) -> None:
        """Should format permissions given as decimal."""
        assert format_permissions(493) == "0755"  # 0o755 in decimal
        assert format_permissions(420) == "0644"  # 0o644 in decimal

    def test_format_masks_file_type_bits(self) -> None:
        """Should mask out file type bits, only showing permission bits."""
        # File type bits + permissions
        file_mode = 0o100644  # Regular file with 0o644 permissions
        assert format_permissions(file_mode) == "0644"

        dir_mode = 0o040755  # Directory with 0o755 permissions
        assert format_permissions(dir_mode) == "0755"

    def test_format_preserves_leading_zeros(self) -> None:
        """Should preserve leading zeros in formatted output."""
        assert format_permissions(0o007) == "0007"
        assert format_permissions(0o070) == "0070"
        assert format_permissions(0o700) == "0700"


class TestSetAndGetPermissions:
    """Tests for set_file_permissions and get_permissions functions."""

    def test_set_and_get_permissions_on_file(self, tmp_path: Path) -> None:
        """Should set and get permissions on a file."""
        test_file = tmp_path / "test.txt"
        test_file.touch()

        set_file_permissions(test_file, 0o644)
        assert get_permissions(test_file) == 0o644

        set_file_permissions(test_file, 0o600)
        assert get_permissions(test_file) == 0o600

    def test_set_and_get_permissions_on_directory(self, tmp_path: Path) -> None:
        """Should set and get permissions on a directory."""
        test_dir = tmp_path / "testdir"
        test_dir.mkdir()

        set_file_permissions(test_dir, 0o755)
        assert get_permissions(test_dir) == 0o755

        set_file_permissions(test_dir, 0o700)
        assert get_permissions(test_dir) == 0o700

    def test_get_permissions_nonexistent_file(self, tmp_path: Path) -> None:
        """Should return 0 for non-existent file."""
        nonexistent = tmp_path / "nonexistent.txt"
        assert get_permissions(nonexistent) == 0

    def test_set_permissions_raises_on_nonexistent(self, tmp_path: Path) -> None:
        """Should raise OSError when setting permissions on non-existent file."""
        nonexistent = tmp_path / "nonexistent.txt"
        with pytest.raises(OSError):
            set_file_permissions(nonexistent, 0o644)


class TestEnsureSecurePermissions:
    """Tests for ensure_secure_permissions function."""

    def test_ensure_secure_permissions_on_regular_file(self, tmp_path: Path) -> None:
        """Should apply default file permissions to regular file."""
        test_file = tmp_path / "file.txt"
        test_file.touch()

        ensure_secure_permissions(test_file)
        assert get_permissions(test_file) == DEFAULT_FILE_PERMS

    def test_ensure_secure_permissions_on_executable(self, tmp_path: Path) -> None:
        """Should apply executable permissions when is_executable=True."""
        test_file = tmp_path / "script.sh"
        test_file.touch()

        ensure_secure_permissions(test_file, is_executable=True)
        assert get_permissions(test_file) == DEFAULT_EXECUTABLE_PERMS

    def test_ensure_secure_permissions_on_directory(self, tmp_path: Path) -> None:
        """Should apply directory permissions to directories."""
        test_dir = tmp_path / "testdir"
        test_dir.mkdir()

        ensure_secure_permissions(test_dir)
        assert get_permissions(test_dir) == DEFAULT_DIR_PERMS

    def test_ensure_secure_permissions_with_custom_modes(self, tmp_path: Path) -> None:
        """Should use custom modes when provided."""
        test_file = tmp_path / "file.txt"
        test_file.touch()

        custom_mode = 0o600
        ensure_secure_permissions(test_file, file_mode=custom_mode)
        assert get_permissions(test_file) == custom_mode

    def test_ensure_secure_permissions_executable_custom_mode(self, tmp_path: Path) -> None:
        """Should use custom executable mode when provided."""
        test_file = tmp_path / "script.sh"
        test_file.touch()

        custom_exec_mode = 0o700
        ensure_secure_permissions(
            test_file,
            is_executable=True,
            executable_mode=custom_exec_mode,
        )
        assert get_permissions(test_file) == custom_exec_mode

    def test_ensure_secure_permissions_directory_custom_mode(self, tmp_path: Path) -> None:
        """Should use custom directory mode when provided."""
        test_dir = tmp_path / "testdir"
        test_dir.mkdir()

        custom_dir_mode = 0o700
        ensure_secure_permissions(test_dir, dir_mode=custom_dir_mode)
        assert get_permissions(test_dir) == custom_dir_mode


class TestPermissionsRoundTrip:
    """Tests for round-trip conversions between formats."""

    def test_parse_and_format_round_trip(self) -> None:
        """Should round-trip parse and format correctly."""
        test_values = ["0755", "0644", "0600", "0777", "0400"]

        for value in test_values:
            parsed = parse_permissions(value)
            formatted = format_permissions(parsed)
            assert formatted == value

    def test_set_get_round_trip(self, tmp_path: Path) -> None:
        """Should round-trip set and get permissions correctly."""
        test_file = tmp_path / "test.txt"
        test_file.touch()

        test_modes = [0o755, 0o644, 0o600, 0o777, 0o400]

        for mode in test_modes:
            set_file_permissions(test_file, mode)
            retrieved = get_permissions(test_file)
            assert retrieved == mode


class TestPermissionsConstants:
    """Tests for permission constants."""

    def test_default_file_perms_value(self) -> None:
        """Should have correct default file permissions."""
        assert DEFAULT_FILE_PERMS == 0o644

    def test_default_dir_perms_value(self) -> None:
        """Should have correct default directory permissions."""
        assert DEFAULT_DIR_PERMS == 0o755

    def test_default_executable_perms_value(self) -> None:
        """Should have correct default executable permissions."""
        assert DEFAULT_EXECUTABLE_PERMS == 0o755


class TestPermissionsIntegration:
    """Integration tests combining multiple permission functions."""

    def test_full_workflow_file(self, tmp_path: Path) -> None:
        """Test complete workflow: parse, set, get, format for file."""
        test_file = tmp_path / "test.txt"
        test_file.touch()

        # Parse permission string
        perms = parse_permissions("0600")

        # Set permissions
        set_file_permissions(test_file, perms)

        # Get permissions
        retrieved = get_permissions(test_file)
        assert retrieved == 0o600

        # Format permissions
        formatted = format_permissions(retrieved)
        assert formatted == "0600"

    def test_full_workflow_directory(self, tmp_path: Path) -> None:
        """Test complete workflow: parse, set, get, format for directory."""
        test_dir = tmp_path / "testdir"
        test_dir.mkdir()

        # Parse permission string
        perms = parse_permissions("0700")

        # Set permissions
        set_file_permissions(test_dir, perms)

        # Get permissions
        retrieved = get_permissions(test_dir)
        assert retrieved == 0o700

        # Format permissions
        formatted = format_permissions(retrieved)
        assert formatted == "0700"

    def test_ensure_secure_then_modify(self, tmp_path: Path) -> None:
        """Test applying secure defaults then modifying."""
        test_file = tmp_path / "test.txt"
        test_file.touch()

        # Apply secure defaults
        ensure_secure_permissions(test_file)
        assert get_permissions(test_file) == DEFAULT_FILE_PERMS

        # Modify permissions
        new_perms = parse_permissions("0400")
        set_file_permissions(test_file, new_perms)
        assert get_permissions(test_file) == 0o400


# 🧱🏗️🔚
