#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for atomic file operations permission handling."""

from __future__ import annotations

import os
from pathlib import Path

from provide.testkit import FoundationTestCase

from provide.foundation.file.atomic import (
    atomic_replace,
    atomic_write,
    atomic_write_text,
)


class TestAtomicPermissions(FoundationTestCase):
    """Test atomic file operations permission handling."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_os_replace_preserves_permissions(self, temp_directory: Path) -> None:
        """Test that os.replace behavior with permissions."""
        target = temp_directory / "target.txt"
        target.write_bytes(b"Original")
        target.chmod(0o600)

        temp = temp_directory / "temp.txt"
        temp.write_bytes(b"New content")
        # Temp file gets default permissions
        temp_mode = temp.stat().st_mode & 0o777

        # os.replace uses the SOURCE file's permissions, not the target's
        temp.replace(target)

        assert target.read_bytes() == b"New content"
        # On macOS/Linux, os.replace uses source file permissions
        assert target.stat().st_mode & 0o777 == temp_mode

    def test_atomic_write_default_preserves_existing(self, temp_directory: Path) -> None:
        """Test atomic_write preserves existing permissions by default."""
        path = temp_directory / "test.txt"
        path.write_bytes(b"Original")
        path.chmod(0o600)

        # Default behavior should preserve
        atomic_write(path, b"New content")

        assert path.read_bytes() == b"New content"
        assert path.stat().st_mode & 0o777 == 0o600

    def test_atomic_write_explicit_preserve_true(self, temp_directory: Path) -> None:
        """Test atomic_write with preserve_mode=True."""
        path = temp_directory / "test.txt"
        path.write_bytes(b"Original")
        path.chmod(0o600)

        atomic_write(path, b"New content", preserve_mode=True)

        assert path.read_bytes() == b"New content"
        assert path.stat().st_mode & 0o777 == 0o600

    def test_atomic_write_preserve_false_on_existing(self, temp_directory: Path) -> None:
        """Test atomic_write with preserve_mode=False on existing file."""
        path = temp_directory / "test.txt"
        path.write_bytes(b"Original")
        path.chmod(0o600)

        # With preserve_mode=False, should NOT preserve 0o600
        atomic_write(path, b"New content", preserve_mode=False)

        assert path.read_bytes() == b"New content"
        # Should get default permissions, not 0o600
        mode = path.stat().st_mode & 0o777
        assert mode != 0o600, f"Mode should not be preserved: {oct(mode)}"
        # Usually defaults to 0o644 or 0o664 depending on umask
        assert mode >= 0o644, f"Mode should be at least 0o644: {oct(mode)}"

    def test_atomic_write_preserve_false_on_new(self, temp_directory: Path) -> None:
        """Test atomic_write with preserve_mode=False on new file."""
        path = temp_directory / "new.txt"

        # Create with preserve_mode=False (shouldn't matter for new files)
        atomic_write(path, b"Content", preserve_mode=False)

        assert path.read_bytes() == b"Content"
        # Should get default permissions
        mode = path.stat().st_mode & 0o777
        assert mode >= 0o644  # At least readable

    def test_atomic_write_explicit_mode_overrides(self, temp_directory: Path) -> None:
        """Test that explicit mode overrides both existing and preserve_mode."""
        path = temp_directory / "test.txt"
        path.write_bytes(b"Original")
        path.chmod(0o777)  # Very permissive

        # Explicit mode should override everything
        atomic_write(path, b"New", mode=0o600, preserve_mode=True)

        assert path.stat().st_mode & 0o777 == 0o600

        # Even with preserve_mode=False
        atomic_write(path, b"Newer", mode=0o644, preserve_mode=False)

        assert path.stat().st_mode & 0o777 == 0o644

    def test_atomic_replace_default_preserves(self, temp_directory: Path) -> None:
        """Test atomic_replace preserves by default."""
        path = temp_directory / "test.txt"
        path.write_bytes(b"Original")
        path.chmod(0o600)

        atomic_replace(path, b"Replaced")

        assert path.read_bytes() == b"Replaced"
        assert path.stat().st_mode & 0o777 == 0o600

    def test_atomic_replace_explicit_preserve_true(self, temp_directory: Path) -> None:
        """Test atomic_replace with preserve_mode=True."""
        path = temp_directory / "test.txt"
        path.write_bytes(b"Original")
        path.chmod(0o600)

        atomic_replace(path, b"Replaced", preserve_mode=True)

        assert path.read_bytes() == b"Replaced"
        assert path.stat().st_mode & 0o777 == 0o600

    def test_atomic_replace_preserve_false(self, temp_directory: Path) -> None:
        """Test atomic_replace with preserve_mode=False."""
        path = temp_directory / "test.txt"
        path.write_bytes(b"Original")
        path.chmod(0o600)

        atomic_replace(path, b"Replaced", preserve_mode=False)

        assert path.read_bytes() == b"Replaced"
        # Should NOT preserve the 0o600 permissions
        mode = path.stat().st_mode & 0o777
        assert mode != 0o600, f"Mode should not be preserved: {oct(mode)}"
        assert mode >= 0o644, f"Mode should be at least 0o644: {oct(mode)}"

    def test_atomic_write_text_preserve_modes(self, temp_directory: Path) -> None:
        """Test atomic_write_text permission handling."""
        path = temp_directory / "test.txt"
        path.write_text("Original")
        path.chmod(0o600)

        # Default preserves
        atomic_write_text(path, "New text")
        assert path.stat().st_mode & 0o777 == 0o600

        # Explicit preserve
        atomic_write_text(path, "Newer text", preserve_mode=True)
        assert path.stat().st_mode & 0o777 == 0o600

        # No preserve
        atomic_write_text(path, "Newest text", preserve_mode=False)
        mode = path.stat().st_mode & 0o777
        assert mode != 0o600, f"Mode should not be preserved: {oct(mode)}"
        assert mode >= 0o644, f"Mode should be at least 0o644: {oct(mode)}"

    def test_permission_preservation_with_umask(self, temp_directory: Path) -> None:
        """Test how umask affects default permissions."""
        original_umask = os.umask(0o022)  # Standard umask
        try:
            path = temp_directory / "test.txt"

            # Create new file with atomic_write - mkstemp creates with 0o600
            # so the umask doesn't affect it unless we're not preserving
            atomic_write(path, b"Content")
            mode = path.stat().st_mode & 0o777
            # For new files, atomic_write uses mkstemp which creates 0o600
            # Unless we explicitly handle this case
            assert mode in (0o600, 0o644), f"Expected 0o600 or 0o644, got {oct(mode)}"

            # Test with preserve_mode=False to get default permissions
            path3 = temp_directory / "test3.txt"
            atomic_write(path3, b"Content", preserve_mode=False)
            mode3 = path3.stat().st_mode & 0o777
            # With preserve_mode=False and umask 0o022, should be 0o644
            assert mode3 == 0o644, f"Expected 0o644 with preserve_mode=False and umask 0o022, got {oct(mode3)}"

            # Now test with different umask
            os.umask(0o077)  # Restrictive umask
            path2 = temp_directory / "test2.txt"
            atomic_write(path2, b"Content", preserve_mode=False)
            mode2 = path2.stat().st_mode & 0o777
            # With umask 0o077, default should be 0o600 (0o666 & ~0o077)
            assert mode2 == 0o600, f"Expected 0o600 with umask 0o077, got {oct(mode2)}"

        finally:
            os.umask(original_umask)  # Restore original umask


# 🧱🏗️🔚
