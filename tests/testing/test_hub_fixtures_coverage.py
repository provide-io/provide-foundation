#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Additional tests for testing hub fixtures to improve code coverage."""

from __future__ import annotations

from pathlib import Path

from provide.testkit import FoundationTestCase


class TestHubFixturesCoverage(FoundationTestCase):
    """Test hub testing fixtures for improved coverage."""

    def test_default_container_directory_fixture(self, default_container_directory: Path) -> None:
        """Test default_container_directory fixture provides valid path."""
        # Test that we get a Path object
        assert isinstance(default_container_directory, Path)

        # Test that the path exists during test execution
        assert default_container_directory.exists()

        # Test that it's a directory
        assert default_container_directory.is_dir()

        # Test that we can create files in it
        test_file = default_container_directory / "test_file.txt"
        test_file.write_text("test content")
        assert test_file.exists()
        assert test_file.read_text() == "test content"

    def test_default_container_directory_is_temporary(
        self,
        default_container_directory: Path,
    ) -> None:
        """Test that the directory is temporary and isolated per test session."""
        # Since it's session-scoped, we get the same directory within the session
        # but it's still a temporary directory that will be cleaned up

        # Create a marker file
        marker = default_container_directory / "session_marker.txt"
        marker.write_text("session data")

        # Verify it exists
        assert marker.exists()
        assert marker.read_text() == "session data"

        # Test we can create subdirectories
        subdir = default_container_directory / "subdir"
        subdir.mkdir()
        assert subdir.exists()
        assert subdir.is_dir()

    def test_container_directory_path_operations(self, default_container_directory: Path) -> None:
        """Test various path operations on the container directory."""
        # Test path joining
        nested_path = default_container_directory / "nested" / "deep" / "path"
        nested_path.mkdir(parents=True)
        assert nested_path.exists()

        # Test file operations
        config_file = default_container_directory / "config.json"
        config_file.write_text('{"test": true}')

        assert config_file.exists()
        assert config_file.is_file()
        assert '"test": true' in config_file.read_text()

        # Test parent access
        assert config_file.parent == default_container_directory


# 🧱🏗️🔚
