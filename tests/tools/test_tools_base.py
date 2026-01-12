#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test-driven development tests for BaseToolManager.

These tests define the expected behavior before implementation."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch
import pytest

from provide.foundation.config import BaseConfig
from provide.foundation.tools.base import (
    BaseToolManager,
    ToolError,
    ToolInstallError,
    ToolMetadata,
    ToolNotFoundError,
    ToolVerificationError,
)


class TestToolMetadata(FoundationTestCase):
    """Tests for ToolMetadata dataclass."""

    def test_metadata_creation(self) -> None:
        """Test creating tool metadata with required fields."""
        metadata = ToolMetadata(
            name="terraform",
            version="1.5.0",
            platform="linux",
            arch="amd64",
        )

        assert metadata.name == "terraform"
        assert metadata.version == "1.5.0"
        assert metadata.platform == "linux"
        assert metadata.arch == "amd64"
        assert metadata.checksum is None
        assert metadata.env_vars == {}
        assert metadata.dependencies == []

    def test_metadata_with_optional_fields(self) -> None:
        """Test metadata with all optional fields."""
        metadata = ToolMetadata(
            name="go",
            version="1.21.0",
            platform="darwin",
            arch="arm64",
            checksum="abc123",
            download_url="https://example.com/go.tar.gz",
            env_vars={"GOPATH": "/usr/local/go"},
            dependencies=["gcc"],
        )

        assert metadata.checksum == "abc123"
        assert metadata.download_url == "https://example.com/go.tar.gz"
        assert metadata.env_vars == {"GOPATH": "/usr/local/go"}
        assert metadata.dependencies == ["gcc"]


class TestBaseToolManager(FoundationTestCase):
    """Tests for BaseToolManager abstract class."""

    @pytest.fixture
    def mock_config(self) -> MagicMock:
        """Create a mock config."""
        return MagicMock(spec=BaseConfig)

    @pytest.fixture
    def concrete_manager(self, mock_config: MagicMock) -> BaseToolManager:
        """Create a concrete implementation of BaseToolManager."""

        class ConcreteToolManager(BaseToolManager):
            tool_name = "testtool"
            executable_name = "testtool"
            supported_platforms: ClassVar[list[str]] = ["linux", "darwin"]

            def get_metadata(self, version: str) -> ToolMetadata:
                return ToolMetadata(
                    name=self.tool_name,
                    version=version,
                    platform="linux",
                    arch="amd64",
                    download_url=f"https://example.com/{version}.tar.gz",
                    checksum="sha256:abcd1234",
                )

            def get_available_versions(self) -> list[str]:
                return ["1.0.0", "1.1.0", "1.2.0", "2.0.0-beta"]

        return ConcreteToolManager(mock_config)

    def test_manager_requires_tool_name(self, mock_config: MagicMock) -> None:
        """Test that manager requires tool_name to be defined."""

        class InvalidManager(BaseToolManager):
            executable_name = "test"

            def get_metadata(self, version: str) -> ToolMetadata:
                return ToolMetadata(name="test", version=version, platform="linux", arch="amd64")

            def get_available_versions(self) -> list[str]:
                return []

        with pytest.raises(ToolError, match="must define tool_name"):
            InvalidManager(mock_config)

    def test_manager_requires_executable_name(self, mock_config: MagicMock) -> None:
        """Test that manager requires executable_name to be defined."""

        class InvalidManager(BaseToolManager):
            tool_name = "test"

            def get_metadata(self, version: str) -> ToolMetadata:
                return ToolMetadata(name="test", version=version, platform="linux", arch="amd64")

            def get_available_versions(self) -> list[str]:
                return []

        with pytest.raises(ToolError, match="must define executable_name"):
            InvalidManager(mock_config)

    def test_resolve_version_latest(self, concrete_manager: BaseToolManager) -> None:
        """Test resolving 'latest' version."""
        with patch.object(concrete_manager.resolver, "resolve") as mock_resolve:
            mock_resolve.return_value = "1.2.0"

            result = concrete_manager.resolve_version("latest")

            assert result == "1.2.0"
            mock_resolve.assert_called_once_with(
                "latest",
                ["1.0.0", "1.1.0", "1.2.0", "2.0.0-beta"],
            )

    def test_resolve_version_not_found(self, concrete_manager: BaseToolManager) -> None:
        """Test resolving non-existent version."""
        with patch.object(concrete_manager.resolver, "resolve") as mock_resolve:
            mock_resolve.return_value = None

            with pytest.raises(ToolNotFoundError, match="Cannot resolve version"):
                concrete_manager.resolve_version("3.0.0")

    def test_get_platform_info(self, concrete_manager: BaseToolManager) -> None:
        """Test getting platform information."""
        with patch("platform.system") as mock_system, patch("platform.machine") as mock_machine:
            mock_system.return_value = "Linux"
            mock_machine.return_value = "x86_64"

            info = concrete_manager.get_platform_info()

            assert info == {"platform": "linux", "arch": "amd64"}

    def test_get_platform_info_darwin_arm(self, concrete_manager: BaseToolManager) -> None:
        """Test platform info for Mac ARM."""
        with patch("platform.system") as mock_system, patch("platform.machine") as mock_machine:
            mock_system.return_value = "Darwin"
            mock_machine.return_value = "arm64"

            info = concrete_manager.get_platform_info()

            assert info == {"platform": "darwin", "arch": "arm64"}

    def test_get_install_path(self, concrete_manager: BaseToolManager) -> None:
        """Test getting installation path for a version."""
        path = concrete_manager.get_install_path("1.5.0")

        assert path == Path.home() / ".provide-foundation" / "tools" / "testtool" / "1.5.0"

    def test_is_installed_true(self, concrete_manager: BaseToolManager, tmp_path: Path) -> None:
        """Test checking if version is installed."""
        with patch.object(concrete_manager, "get_install_path") as mock_path:
            install_dir = tmp_path / "testtool"
            bin_dir = install_dir / "bin"
            bin_dir.mkdir(parents=True)
            (bin_dir / "testtool").touch()

            mock_path.return_value = install_dir

            assert concrete_manager.is_installed("1.0.0") is True

    def test_is_installed_false(self, concrete_manager: BaseToolManager, tmp_path: Path) -> None:
        """Test checking if version is not installed."""
        with patch.object(concrete_manager, "get_install_path") as mock_path:
            mock_path.return_value = tmp_path / "notexist"

            assert concrete_manager.is_installed("1.0.0") is False

    @patch("provide.foundation.tools.base.Path")
    async def test_install_cached(self, mock_path_class: MagicMock, concrete_manager: BaseToolManager) -> None:
        """Test installing from cache."""
        cached_path = MagicMock(spec=Path)

        with patch.object(concrete_manager.cache, "get") as mock_get:
            mock_get.return_value = cached_path

            result = await concrete_manager.install("1.0.0")

            assert result == cached_path
            mock_get.assert_called_once_with("testtool", "1.0.0")

    async def test_install_download_and_verify(
        self, concrete_manager: BaseToolManager, tmp_path: Path
    ) -> None:
        """Test full installation with download and verification."""
        artifact_path = tmp_path / "artifact.tar.gz"
        install_path = tmp_path / "install"

        with (
            patch.object(concrete_manager.cache, "get") as mock_cache_get,
            patch.object(concrete_manager.downloader, "download_with_progress") as mock_download,
            patch.object(concrete_manager.verifier, "verify_checksum") as mock_verify,
            patch.object(concrete_manager.installer, "install") as mock_install,
            patch.object(concrete_manager.cache, "store") as mock_cache_store,
        ):
            mock_cache_get.return_value = None
            mock_download.return_value = artifact_path
            mock_verify.return_value = True
            mock_install.return_value = install_path

            # Create the artifact file
            artifact_path.touch()

            result = await concrete_manager.install("1.0.0")

            assert result == install_path
            mock_download.assert_called_once()
            mock_verify.assert_called_once_with(artifact_path, "sha256:abcd1234")
            mock_install.assert_called_once()
            mock_cache_store.assert_called_once_with("testtool", "1.0.0", install_path)

    async def test_install_verification_fails(self, concrete_manager: BaseToolManager, tmp_path: Path) -> None:
        """Test installation fails when verification fails."""
        artifact_path = tmp_path / "artifact.tar.gz"

        with (
            patch.object(concrete_manager.cache, "get") as mock_cache_get,
            patch.object(concrete_manager.downloader, "download_with_progress") as mock_download,
            patch.object(concrete_manager.verifier, "verify_checksum") as mock_verify,
        ):
            mock_cache_get.return_value = None
            mock_download.return_value = artifact_path
            mock_verify.return_value = False

            # Create the artifact file
            artifact_path.touch()

            with pytest.raises(ToolVerificationError, match="Checksum verification failed"):
                await concrete_manager.install("1.0.0")

            # Artifact should be deleted
            assert not artifact_path.exists()

    async def test_install_no_download_url(self, concrete_manager: BaseToolManager) -> None:
        """Test installation fails when no download URL available."""

        def get_metadata_no_url(version: str) -> ToolMetadata:
            return ToolMetadata(
                name="testtool",
                version=version,
                platform="linux",
                arch="amd64",
            )

        with (
            patch.object(concrete_manager.cache, "get") as mock_cache_get,
            patch.object(concrete_manager, "get_metadata", get_metadata_no_url),
        ):
            mock_cache_get.return_value = None

            with pytest.raises(ToolInstallError, match="No download URL"):
                await concrete_manager.install("1.0.0")

    def test_uninstall_success(self, concrete_manager: BaseToolManager, tmp_path: Path) -> None:
        """Test successful uninstallation."""
        install_path = tmp_path / "testtool"
        install_path.mkdir(parents=True)
        (install_path / "bin").mkdir()
        (install_path / "bin" / "testtool").touch()

        with (
            patch.object(concrete_manager, "get_install_path") as mock_path,
            patch.object(concrete_manager.cache, "invalidate") as mock_invalidate,
        ):
            mock_path.return_value = install_path

            result = concrete_manager.uninstall("1.0.0")

            assert result is True
            assert not install_path.exists()
            mock_invalidate.assert_called_once_with("testtool", "1.0.0")

    def test_uninstall_not_found(self, concrete_manager: BaseToolManager, tmp_path: Path) -> None:
        """Test uninstalling non-existent version."""
        with (
            patch.object(concrete_manager, "get_install_path") as mock_path,
            patch.object(concrete_manager.cache, "invalidate") as mock_invalidate,
        ):
            mock_path.return_value = tmp_path / "notexist"

            result = concrete_manager.uninstall("1.0.0")

            assert result is False
            mock_invalidate.assert_called_once_with("testtool", "1.0.0")

    def test_lazy_loading_properties(self, concrete_manager: BaseToolManager) -> None:
        """Test that components are lazy-loaded."""
        # Initially None
        assert concrete_manager._cache is None
        assert concrete_manager._downloader is None
        assert concrete_manager._verifier is None
        assert concrete_manager._installer is None
        assert concrete_manager._resolver is None

        # Access them
        _ = concrete_manager.cache
        _ = concrete_manager.downloader
        _ = concrete_manager.verifier
        _ = concrete_manager.installer
        _ = concrete_manager.resolver

        # Now they should be initialized
        assert concrete_manager._cache is not None
        assert concrete_manager._downloader is not None
        assert concrete_manager._verifier is not None
        assert concrete_manager._installer is not None
        assert concrete_manager._resolver is not None


# 🧱🏗️🔚
