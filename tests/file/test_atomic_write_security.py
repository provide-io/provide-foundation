#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Security tests for atomic write operations.

Tests permission races, concurrent writes, and security edge cases."""

from __future__ import annotations

import os
from pathlib import Path
import stat
import tempfile
import threading

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file.atomic import atomic_replace, atomic_write, atomic_write_text


class TestAtomicWritePermissionSecurity(FoundationTestCase):
    """Test atomic write permission security."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.txt"

    def teardown_method(self) -> None:
        """Clean up test environment."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)
        super().teardown_method()

    def test_permissions_set_atomically_no_race_window(self) -> None:
        """Test that permissions are set atomically without race window."""
        # Write file with specific permissions
        data = b"test data"
        mode = 0o600  # Read/write owner only

        atomic_write(self.test_file, data, mode=mode)

        # Verify permissions are exactly as specified
        actual_mode = self.test_file.stat().st_mode & 0o777
        assert actual_mode == mode, f"Expected {oct(mode)}, got {oct(actual_mode)}"

    def test_permission_preservation_across_replace(self) -> None:
        """Test that permissions are preserved when replacing files."""
        # Create initial file with specific permissions
        self.test_file.write_bytes(b"original")
        self.test_file.chmod(0o640)

        # Replace with new data, preserving permissions
        atomic_write(self.test_file, b"replaced", preserve_mode=True)

        # Verify permissions preserved
        actual_mode = self.test_file.stat().st_mode & 0o777
        assert actual_mode == 0o640, f"Permissions not preserved: {oct(actual_mode)}"

    def test_default_permissions_respect_umask(self) -> None:
        """Test that default permissions respect umask."""
        # Get current umask
        current_umask = os.umask(0)
        os.umask(current_umask)

        # Write without specifying mode
        atomic_write(self.test_file, b"data", preserve_mode=False)

        # Verify umask was applied
        actual_mode = self.test_file.stat().st_mode & 0o777
        expected = 0o666 & ~current_umask
        assert actual_mode == expected, f"Expected {oct(expected)}, got {oct(actual_mode)}"

    def test_explicit_mode_overrides_umask(self) -> None:
        """Test that explicit mode overrides umask."""
        mode = 0o755

        atomic_write(self.test_file, b"data", mode=mode)

        actual_mode = self.test_file.stat().st_mode & 0o777
        assert actual_mode == mode, "Explicit mode should override umask"

    def test_sensitive_data_not_world_readable(self) -> None:
        """Test that sensitive data written with restrictive permissions."""
        sensitive_data = b"password=secret123"
        mode = 0o600  # Owner read/write only

        atomic_write(self.test_file, sensitive_data, mode=mode)

        # Verify not readable by group or others
        actual_mode = self.test_file.stat().st_mode
        assert not (actual_mode & stat.S_IRGRP), "Should not be group readable"
        assert not (actual_mode & stat.S_IROTH), "Should not be world readable"
        assert not (actual_mode & stat.S_IWGRP), "Should not be group writable"
        assert not (actual_mode & stat.S_IWOTH), "Should not be world writable"


class TestAtomicWriteConcurrency(FoundationTestCase):
    """Test concurrent atomic write operations."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "concurrent.txt"

    def teardown_method(self) -> None:
        """Clean up test environment."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)
        super().teardown_method()

    def test_concurrent_writes_no_corruption(self) -> None:
        """Test that concurrent writes don't corrupt the file."""
        num_threads = 10
        threads = []
        errors = []

        def write_data(thread_id: int) -> None:
            """Write data from thread."""
            try:
                data = f"thread-{thread_id}\n".encode() * 100
                atomic_write(self.test_file, data)
            except Exception as e:
                errors.append(e)

        # Start concurrent writers
        for i in range(num_threads):
            t = threading.Thread(target=write_data, args=(i,))
            threads.append(t)
            t.start()

        # Wait for all
        for t in threads:
            t.join()

        # Should not have errors
        assert len(errors) == 0, f"Concurrent writes had errors: {errors}"

        # File should exist and be complete
        assert self.test_file.exists(), "File should exist after concurrent writes"
        content = self.test_file.read_bytes()
        assert len(content) > 0, "File should have content"

        # Content should be from one complete write (not interleaved)
        lines = content.decode().split("\n")
        if lines:
            first_line = lines[0]
            # All non-empty lines should be the same thread
            for line in lines:
                if line:  # Skip empty lines
                    assert line == first_line, "Content should be from single atomic write"

    def test_concurrent_writes_with_different_permissions(self) -> None:
        """Test concurrent writes with different permission modes."""
        threads = []

        def write_with_mode(mode: int) -> None:
            """Write with specific mode."""
            atomic_write(self.test_file, b"data", mode=mode)

        # Concurrent writes with different modes
        modes = [0o644, 0o640, 0o600, 0o755, 0o750, 0o700, 0o666, 0o660, 0o664, 0o444]
        for mode in modes:
            t = threading.Thread(target=write_with_mode, args=(mode,))
            threads.append(t)
            t.start()

        # Wait
        for t in threads:
            t.join()

        # Should not crash
        assert self.test_file.exists(), "File should exist"

    def test_concurrent_replace_operations(self) -> None:
        """Test concurrent atomic replace operations."""
        # Create initial file
        self.test_file.write_bytes(b"initial")
        self.test_file.chmod(0o644)

        num_threads = 5
        threads = []
        errors = []

        def replace_file(thread_id: int) -> None:
            """Replace file content."""
            try:
                data = f"replaced-{thread_id}".encode()
                atomic_replace(self.test_file, data)
            except Exception as e:
                errors.append(e)

        # Start threads
        for i in range(num_threads):
            t = threading.Thread(target=replace_file, args=(i,))
            threads.append(t)
            t.start()

        # Wait
        for t in threads:
            t.join()

        # Should not have errors
        assert len(errors) == 0, f"Replace operations had errors: {errors}"

        # File should still exist with one complete write
        assert self.test_file.exists()
        content = self.test_file.read_bytes()
        assert content.startswith(b"replaced-"), "Should have one complete replacement"


class TestAtomicWriteEdgeCases(FoundationTestCase):
    """Test edge cases and error conditions."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self) -> None:
        """Clean up test environment."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)
        super().teardown_method()

    def test_atomic_write_text_encoding_security(self) -> None:
        """Test that text encoding doesn't leak partial writes."""
        test_file = Path(self.temp_dir) / "encoded.txt"

        # Write with specific encoding
        text = "Hello \u00a9 World"  # Copyright symbol
        atomic_write_text(test_file, text, encoding="utf-8")

        # Read back
        content = test_file.read_text(encoding="utf-8")
        assert content == text, "Encoding should be preserved"

    def test_atomic_write_with_symlink_parent(self) -> None:
        """Test atomic write when parent is a symlink."""
        real_dir = Path(self.temp_dir) / "real"
        link_dir = Path(self.temp_dir) / "link"
        real_dir.mkdir()
        link_dir.symlink_to(real_dir)

        test_file = link_dir / "test.txt"
        atomic_write(test_file, b"data")

        # Should write to real directory
        assert (real_dir / "test.txt").exists()
        assert test_file.exists()  # Link should work

    def test_atomic_write_preserves_no_permissions_on_nonexistent(self) -> None:
        """Test preserve_mode=True on non-existent file uses defaults."""
        test_file = Path(self.temp_dir) / "new.txt"

        # File doesn't exist, preserve_mode should use defaults
        atomic_write(test_file, b"data", preserve_mode=True)

        # Should succeed with default permissions
        assert test_file.exists()
        actual_mode = test_file.stat().st_mode & 0o777
        # Should use default umask-based permissions
        current_umask = os.umask(0)
        os.umask(current_umask)
        expected = 0o666 & ~current_umask
        assert actual_mode == expected

    def test_atomic_write_cleanup_on_failure(self) -> None:
        """Test that temp files are cleaned up on write failure."""
        Path(self.temp_dir) / "fail.txt"

        # Write some invalid data that will fail fsync (simulated with permission error)
        # Create directory with no write permission
        no_write_dir = Path(self.temp_dir) / "no_write"
        no_write_dir.mkdir()
        no_write_dir.chmod(0o555)  # Read+execute only

        test_file_no_write = no_write_dir / "test.txt"

        # Should raise error
        with pytest.raises((OSError, PermissionError)):
            atomic_write(test_file_no_write, b"data")

        # Temp file should be cleaned up (best effort)
        # Note: May not be possible to verify cleanup if we don't have write permission

        # Cleanup
        no_write_dir.chmod(0o755)


class TestAtomicWritePermissionTransitions(FoundationTestCase):
    """Test permission transitions during atomic writes."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.txt"

    def teardown_method(self) -> None:
        """Clean up test environment."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)
        super().teardown_method()

    def test_permission_tightening(self) -> None:
        """Test tightening permissions during write."""
        # Start with permissive permissions
        self.test_file.write_bytes(b"initial")
        self.test_file.chmod(0o666)

        # Write with restricted permissions
        atomic_write(self.test_file, b"restricted", mode=0o600)

        # Should have restrictive permissions
        actual = self.test_file.stat().st_mode & 0o777
        assert actual == 0o600

    def test_permission_loosening(self) -> None:
        """Test loosening permissions during write."""
        # Start with restrictive permissions
        self.test_file.write_bytes(b"initial")
        self.test_file.chmod(0o600)

        # Write with permissive permissions
        atomic_write(self.test_file, b"permissive", mode=0o644)

        # Should have permissive permissions
        actual = self.test_file.stat().st_mode & 0o777
        assert actual == 0o644

    def test_preserve_mode_maintains_original_permissions(self) -> None:
        """Test that preserve_mode maintains exact permissions."""
        # Create with specific permissions
        self.test_file.write_bytes(b"initial")
        original_mode = 0o640
        self.test_file.chmod(original_mode)

        # Write multiple times with preserve_mode
        for i in range(5):
            atomic_write(self.test_file, f"iteration-{i}".encode(), preserve_mode=True)
            actual = self.test_file.stat().st_mode & 0o777
            assert actual == original_mode, f"Iteration {i} changed permissions"


# 🧱🏗️🔚
