#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Base classes for tool management.

This module provides the foundation for tool managers, including
the base manager class and metadata structures."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from attrs import define, field

from provide.foundation.config import BaseConfig
from provide.foundation.errors import FoundationError
from provide.foundation.logger import get_logger

if TYPE_CHECKING:
    from provide.foundation.tools.cache import ToolCache
    from provide.foundation.tools.downloader import ToolDownloader
    from provide.foundation.tools.installer import ToolInstaller
    from provide.foundation.tools.resolver import VersionResolver
    from provide.foundation.tools.verifier import ToolVerifier

log = get_logger(__name__)


class ToolError(FoundationError):
    """Base exception for tool-related errors."""


class ToolNotFoundError(ToolError):
    """Raised when a tool or version cannot be found."""


class ToolInstallError(ToolError):
    """Raised when tool installation fails."""


class ToolVerificationError(ToolError):
    """Raised when tool verification fails."""


@define(slots=True, kw_only=True)
class ToolMetadata:
    """Metadata about a tool version.

    Attributes:
        name: Tool name (e.g., "terraform").
        version: Version string (e.g., "1.5.0").
        platform: Platform identifier (e.g., "linux", "darwin").
        arch: Architecture (e.g., "amd64", "arm64").
        checksum: Optional checksum for verification.
        signature: Optional GPG/PGP signature.
        download_url: URL to download the tool.
        checksum_url: URL to download checksums file.
        install_path: Where the tool is/will be installed.
        env_vars: Environment variables to set.
        dependencies: Other tools this depends on.
        executable_name: Name of the executable file.

    """

    name: str
    version: str
    platform: str
    arch: str
    checksum: str | None = None
    signature: str | None = None
    download_url: str | None = None
    checksum_url: str | None = None
    install_path: Path | None = None
    env_vars: dict[str, str] = field(factory=dict)
    dependencies: list[str] = field(factory=list)
    executable_name: str | None = None


class BaseToolManager(ABC):
    """Abstract base class for tool managers.

    Provides common functionality for downloading, verifying, and installing
    development tools. Subclasses must implement platform-specific logic.

    Attributes:
        config: Configuration object.
        tool_name: Name of the tool being managed.
        executable_name: Name of the executable file.
        supported_platforms: List of supported platforms.

    """

    # Class attributes to be overridden by subclasses
    tool_name: str = ""
    executable_name: str = ""
    supported_platforms: ClassVar[list[str]] = ["linux", "darwin", "windows"]

    def __init__(self, config: BaseConfig) -> None:
        """Initialize the tool manager.

        Args:
            config: Configuration object containing settings.

        """
        if not self.tool_name:
            raise ToolError("Subclass must define tool_name")
        if not self.executable_name:
            raise ToolError("Subclass must define executable_name")

        self.config = config

        # Lazy-load components to avoid circular imports
        self._cache: ToolCache | None = None
        self._downloader: ToolDownloader | None = None
        self._verifier: ToolVerifier | None = None
        self._installer: ToolInstaller | None = None
        self._resolver: VersionResolver | None = None

        log.debug(f"Initialized {self.tool_name} manager")

    @property
    def cache(self) -> ToolCache:
        """Get or create cache instance."""
        if self._cache is None:
            from provide.foundation.tools.cache import ToolCache

            self._cache = ToolCache()
        return self._cache

    @property
    def downloader(self) -> ToolDownloader:
        """Get or create downloader instance."""
        if self._downloader is None:
            from provide.foundation.hub import get_hub
            from provide.foundation.tools.downloader import ToolDownloader
            from provide.foundation.transport import UniversalClient

            self._downloader = ToolDownloader(UniversalClient(hub=get_hub()))
        return self._downloader

    @property
    def verifier(self) -> ToolVerifier:
        """Get or create verifier instance."""
        if self._verifier is None:
            from provide.foundation.tools.verifier import ToolVerifier

            self._verifier = ToolVerifier()
        return self._verifier

    @property
    def installer(self) -> ToolInstaller:
        """Get or create installer instance."""
        if self._installer is None:
            from provide.foundation.tools.installer import ToolInstaller

            self._installer = ToolInstaller()
        return self._installer

    @property
    def resolver(self) -> VersionResolver:
        """Get or create version resolver instance."""
        if self._resolver is None:
            from provide.foundation.tools.resolver import VersionResolver

            self._resolver = VersionResolver()
        return self._resolver

    @abstractmethod
    def get_metadata(self, version: str) -> ToolMetadata:
        """Get metadata for a specific version.

        Args:
            version: Version string to get metadata for.

        Returns:
            ToolMetadata object with download URLs and checksums.

        """

    @abstractmethod
    def get_available_versions(self) -> list[str]:
        """Get list of available versions from upstream.

        Returns:
            List of version strings available for download.

        """

    def resolve_version(self, spec: str) -> str:
        """Resolve a version specification to a concrete version.

        Args:
            spec: Version specification (e.g., "latest", "~1.5.0").

        Returns:
            Concrete version string.

        Raises:
            ToolNotFoundError: If version cannot be resolved.

        """
        available = self.get_available_versions()
        if not available:
            raise ToolNotFoundError(f"No versions available for {self.tool_name}")

        resolved = self.resolver.resolve(spec, available)
        if not resolved:
            raise ToolNotFoundError(f"Cannot resolve version '{spec}' for {self.tool_name}")

        log.debug(f"Resolved {self.tool_name} version {spec} to {resolved}")
        return resolved

    async def install(self, version: str = "latest", force: bool = False) -> Path:
        """Install a specific version of the tool.

        Args:
            version: Version to install (default: "latest").
            force: Force reinstall even if cached.

        Returns:
            Path to the installed tool.

        Raises:
            ToolInstallError: If installation fails.

        """
        # Resolve version
        if version in ["latest", "stable", "dev"] or version.startswith(("~", "^")):
            version = self.resolve_version(version)

        # Check cache unless forced
        if not force and (cached_path := self.cache.get(self.tool_name, version)):
            log.info(f"Using cached {self.tool_name} {version}")
            return cached_path

        log.info(f"Installing {self.tool_name} {version}")

        # Get metadata
        metadata = self.get_metadata(version)
        if not metadata.download_url:
            raise ToolInstallError(f"No download URL for {self.tool_name} {version}")

        # Download to secure temporary directory
        from provide.foundation.file.temp import system_temp_dir

        download_path = system_temp_dir() / f"{self.tool_name}-{version}"
        artifact_path = await self.downloader.download_with_progress(
            metadata.download_url,
            download_path,
            metadata.checksum,
        )

        # Verify if checksum provided
        if metadata.checksum and not self.verifier.verify_checksum(artifact_path, metadata.checksum):
            artifact_path.unlink()
            raise ToolVerificationError(f"Checksum verification failed for {self.tool_name} {version}")

        # Install
        install_path = self.installer.install(artifact_path, metadata)

        # Cache the installation
        self.cache.store(self.tool_name, version, install_path)

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    def uninstall(self, version: str) -> bool:
        """Uninstall a specific version.

        Args:
            version: Version to uninstall.

        Returns:
            True if uninstalled, False if not found.

        """
        # Invalidate cache
        self.cache.invalidate(self.tool_name, version)

        # Remove from filesystem
        install_path = self.get_install_path(version)
        if install_path.exists():
            import shutil

            shutil.rmtree(install_path)
            log.info(f"Uninstalled {self.tool_name} {version}")
            return True

        return False

    def get_install_path(self, version: str) -> Path:
        """Get the installation path for a version.

        Args:
            version: Version string.

        Returns:
            Path where the version is/will be installed.

        """
        base_path = Path.home() / ".provide-foundation" / "tools" / self.tool_name / version
        return base_path

    def is_installed(self, version: str) -> bool:
        """Check if a version is installed.

        Args:
            version: Version to check.

        Returns:
            True if installed, False otherwise.

        """
        install_path = self.get_install_path(version)
        executable = install_path / "bin" / self.executable_name
        return executable.exists()

    def get_platform_info(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system == "darwin":
            system = "darwin"
        elif system == "linux":
            system = "linux"
        elif system == "windows":
            system = "windows"

        machine = platform.machine().lower()
        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}


# 🧱🏗️🔚
