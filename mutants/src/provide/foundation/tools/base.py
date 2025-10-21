# provide/foundation/tools/base.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Base classes for tool management.

This module provides the foundation for tool managers, including
the base manager class and metadata structures.
"""

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    def xǁBaseToolManagerǁ__init____mutmut_orig(self, config: BaseConfig) -> None:
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

    def xǁBaseToolManagerǁ__init____mutmut_1(self, config: BaseConfig) -> None:
        """Initialize the tool manager.

        Args:
            config: Configuration object containing settings.

        """
        if self.tool_name:
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

    def xǁBaseToolManagerǁ__init____mutmut_2(self, config: BaseConfig) -> None:
        """Initialize the tool manager.

        Args:
            config: Configuration object containing settings.

        """
        if not self.tool_name:
            raise ToolError(None)
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

    def xǁBaseToolManagerǁ__init____mutmut_3(self, config: BaseConfig) -> None:
        """Initialize the tool manager.

        Args:
            config: Configuration object containing settings.

        """
        if not self.tool_name:
            raise ToolError("XXSubclass must define tool_nameXX")
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

    def xǁBaseToolManagerǁ__init____mutmut_4(self, config: BaseConfig) -> None:
        """Initialize the tool manager.

        Args:
            config: Configuration object containing settings.

        """
        if not self.tool_name:
            raise ToolError("subclass must define tool_name")
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

    def xǁBaseToolManagerǁ__init____mutmut_5(self, config: BaseConfig) -> None:
        """Initialize the tool manager.

        Args:
            config: Configuration object containing settings.

        """
        if not self.tool_name:
            raise ToolError("SUBCLASS MUST DEFINE TOOL_NAME")
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

    def xǁBaseToolManagerǁ__init____mutmut_6(self, config: BaseConfig) -> None:
        """Initialize the tool manager.

        Args:
            config: Configuration object containing settings.

        """
        if not self.tool_name:
            raise ToolError("Subclass must define tool_name")
        if self.executable_name:
            raise ToolError("Subclass must define executable_name")

        self.config = config

        # Lazy-load components to avoid circular imports
        self._cache: ToolCache | None = None
        self._downloader: ToolDownloader | None = None
        self._verifier: ToolVerifier | None = None
        self._installer: ToolInstaller | None = None
        self._resolver: VersionResolver | None = None

        log.debug(f"Initialized {self.tool_name} manager")

    def xǁBaseToolManagerǁ__init____mutmut_7(self, config: BaseConfig) -> None:
        """Initialize the tool manager.

        Args:
            config: Configuration object containing settings.

        """
        if not self.tool_name:
            raise ToolError("Subclass must define tool_name")
        if not self.executable_name:
            raise ToolError(None)

        self.config = config

        # Lazy-load components to avoid circular imports
        self._cache: ToolCache | None = None
        self._downloader: ToolDownloader | None = None
        self._verifier: ToolVerifier | None = None
        self._installer: ToolInstaller | None = None
        self._resolver: VersionResolver | None = None

        log.debug(f"Initialized {self.tool_name} manager")

    def xǁBaseToolManagerǁ__init____mutmut_8(self, config: BaseConfig) -> None:
        """Initialize the tool manager.

        Args:
            config: Configuration object containing settings.

        """
        if not self.tool_name:
            raise ToolError("Subclass must define tool_name")
        if not self.executable_name:
            raise ToolError("XXSubclass must define executable_nameXX")

        self.config = config

        # Lazy-load components to avoid circular imports
        self._cache: ToolCache | None = None
        self._downloader: ToolDownloader | None = None
        self._verifier: ToolVerifier | None = None
        self._installer: ToolInstaller | None = None
        self._resolver: VersionResolver | None = None

        log.debug(f"Initialized {self.tool_name} manager")

    def xǁBaseToolManagerǁ__init____mutmut_9(self, config: BaseConfig) -> None:
        """Initialize the tool manager.

        Args:
            config: Configuration object containing settings.

        """
        if not self.tool_name:
            raise ToolError("Subclass must define tool_name")
        if not self.executable_name:
            raise ToolError("subclass must define executable_name")

        self.config = config

        # Lazy-load components to avoid circular imports
        self._cache: ToolCache | None = None
        self._downloader: ToolDownloader | None = None
        self._verifier: ToolVerifier | None = None
        self._installer: ToolInstaller | None = None
        self._resolver: VersionResolver | None = None

        log.debug(f"Initialized {self.tool_name} manager")

    def xǁBaseToolManagerǁ__init____mutmut_10(self, config: BaseConfig) -> None:
        """Initialize the tool manager.

        Args:
            config: Configuration object containing settings.

        """
        if not self.tool_name:
            raise ToolError("Subclass must define tool_name")
        if not self.executable_name:
            raise ToolError("SUBCLASS MUST DEFINE EXECUTABLE_NAME")

        self.config = config

        # Lazy-load components to avoid circular imports
        self._cache: ToolCache | None = None
        self._downloader: ToolDownloader | None = None
        self._verifier: ToolVerifier | None = None
        self._installer: ToolInstaller | None = None
        self._resolver: VersionResolver | None = None

        log.debug(f"Initialized {self.tool_name} manager")

    def xǁBaseToolManagerǁ__init____mutmut_11(self, config: BaseConfig) -> None:
        """Initialize the tool manager.

        Args:
            config: Configuration object containing settings.

        """
        if not self.tool_name:
            raise ToolError("Subclass must define tool_name")
        if not self.executable_name:
            raise ToolError("Subclass must define executable_name")

        self.config = None

        # Lazy-load components to avoid circular imports
        self._cache: ToolCache | None = None
        self._downloader: ToolDownloader | None = None
        self._verifier: ToolVerifier | None = None
        self._installer: ToolInstaller | None = None
        self._resolver: VersionResolver | None = None

        log.debug(f"Initialized {self.tool_name} manager")

    def xǁBaseToolManagerǁ__init____mutmut_12(self, config: BaseConfig) -> None:
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
        self._cache: ToolCache | None = ""
        self._downloader: ToolDownloader | None = None
        self._verifier: ToolVerifier | None = None
        self._installer: ToolInstaller | None = None
        self._resolver: VersionResolver | None = None

        log.debug(f"Initialized {self.tool_name} manager")

    def xǁBaseToolManagerǁ__init____mutmut_13(self, config: BaseConfig) -> None:
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
        self._downloader: ToolDownloader | None = ""
        self._verifier: ToolVerifier | None = None
        self._installer: ToolInstaller | None = None
        self._resolver: VersionResolver | None = None

        log.debug(f"Initialized {self.tool_name} manager")

    def xǁBaseToolManagerǁ__init____mutmut_14(self, config: BaseConfig) -> None:
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
        self._verifier: ToolVerifier | None = ""
        self._installer: ToolInstaller | None = None
        self._resolver: VersionResolver | None = None

        log.debug(f"Initialized {self.tool_name} manager")

    def xǁBaseToolManagerǁ__init____mutmut_15(self, config: BaseConfig) -> None:
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
        self._installer: ToolInstaller | None = ""
        self._resolver: VersionResolver | None = None

        log.debug(f"Initialized {self.tool_name} manager")

    def xǁBaseToolManagerǁ__init____mutmut_16(self, config: BaseConfig) -> None:
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
        self._resolver: VersionResolver | None = ""

        log.debug(f"Initialized {self.tool_name} manager")

    def xǁBaseToolManagerǁ__init____mutmut_17(self, config: BaseConfig) -> None:
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

        log.debug(None)
    
    xǁBaseToolManagerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolManagerǁ__init____mutmut_1': xǁBaseToolManagerǁ__init____mutmut_1, 
        'xǁBaseToolManagerǁ__init____mutmut_2': xǁBaseToolManagerǁ__init____mutmut_2, 
        'xǁBaseToolManagerǁ__init____mutmut_3': xǁBaseToolManagerǁ__init____mutmut_3, 
        'xǁBaseToolManagerǁ__init____mutmut_4': xǁBaseToolManagerǁ__init____mutmut_4, 
        'xǁBaseToolManagerǁ__init____mutmut_5': xǁBaseToolManagerǁ__init____mutmut_5, 
        'xǁBaseToolManagerǁ__init____mutmut_6': xǁBaseToolManagerǁ__init____mutmut_6, 
        'xǁBaseToolManagerǁ__init____mutmut_7': xǁBaseToolManagerǁ__init____mutmut_7, 
        'xǁBaseToolManagerǁ__init____mutmut_8': xǁBaseToolManagerǁ__init____mutmut_8, 
        'xǁBaseToolManagerǁ__init____mutmut_9': xǁBaseToolManagerǁ__init____mutmut_9, 
        'xǁBaseToolManagerǁ__init____mutmut_10': xǁBaseToolManagerǁ__init____mutmut_10, 
        'xǁBaseToolManagerǁ__init____mutmut_11': xǁBaseToolManagerǁ__init____mutmut_11, 
        'xǁBaseToolManagerǁ__init____mutmut_12': xǁBaseToolManagerǁ__init____mutmut_12, 
        'xǁBaseToolManagerǁ__init____mutmut_13': xǁBaseToolManagerǁ__init____mutmut_13, 
        'xǁBaseToolManagerǁ__init____mutmut_14': xǁBaseToolManagerǁ__init____mutmut_14, 
        'xǁBaseToolManagerǁ__init____mutmut_15': xǁBaseToolManagerǁ__init____mutmut_15, 
        'xǁBaseToolManagerǁ__init____mutmut_16': xǁBaseToolManagerǁ__init____mutmut_16, 
        'xǁBaseToolManagerǁ__init____mutmut_17': xǁBaseToolManagerǁ__init____mutmut_17
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolManagerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBaseToolManagerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁBaseToolManagerǁ__init____mutmut_orig)
    xǁBaseToolManagerǁ__init____mutmut_orig.__name__ = 'xǁBaseToolManagerǁ__init__'

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

    def xǁBaseToolManagerǁresolve_version__mutmut_orig(self, spec: str) -> str:
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

    def xǁBaseToolManagerǁresolve_version__mutmut_1(self, spec: str) -> str:
        """Resolve a version specification to a concrete version.

        Args:
            spec: Version specification (e.g., "latest", "~1.5.0").

        Returns:
            Concrete version string.

        Raises:
            ToolNotFoundError: If version cannot be resolved.

        """
        available = None
        if not available:
            raise ToolNotFoundError(f"No versions available for {self.tool_name}")

        resolved = self.resolver.resolve(spec, available)
        if not resolved:
            raise ToolNotFoundError(f"Cannot resolve version '{spec}' for {self.tool_name}")

        log.debug(f"Resolved {self.tool_name} version {spec} to {resolved}")
        return resolved

    def xǁBaseToolManagerǁresolve_version__mutmut_2(self, spec: str) -> str:
        """Resolve a version specification to a concrete version.

        Args:
            spec: Version specification (e.g., "latest", "~1.5.0").

        Returns:
            Concrete version string.

        Raises:
            ToolNotFoundError: If version cannot be resolved.

        """
        available = self.get_available_versions()
        if available:
            raise ToolNotFoundError(f"No versions available for {self.tool_name}")

        resolved = self.resolver.resolve(spec, available)
        if not resolved:
            raise ToolNotFoundError(f"Cannot resolve version '{spec}' for {self.tool_name}")

        log.debug(f"Resolved {self.tool_name} version {spec} to {resolved}")
        return resolved

    def xǁBaseToolManagerǁresolve_version__mutmut_3(self, spec: str) -> str:
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
            raise ToolNotFoundError(None)

        resolved = self.resolver.resolve(spec, available)
        if not resolved:
            raise ToolNotFoundError(f"Cannot resolve version '{spec}' for {self.tool_name}")

        log.debug(f"Resolved {self.tool_name} version {spec} to {resolved}")
        return resolved

    def xǁBaseToolManagerǁresolve_version__mutmut_4(self, spec: str) -> str:
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

        resolved = None
        if not resolved:
            raise ToolNotFoundError(f"Cannot resolve version '{spec}' for {self.tool_name}")

        log.debug(f"Resolved {self.tool_name} version {spec} to {resolved}")
        return resolved

    def xǁBaseToolManagerǁresolve_version__mutmut_5(self, spec: str) -> str:
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

        resolved = self.resolver.resolve(None, available)
        if not resolved:
            raise ToolNotFoundError(f"Cannot resolve version '{spec}' for {self.tool_name}")

        log.debug(f"Resolved {self.tool_name} version {spec} to {resolved}")
        return resolved

    def xǁBaseToolManagerǁresolve_version__mutmut_6(self, spec: str) -> str:
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

        resolved = self.resolver.resolve(spec, None)
        if not resolved:
            raise ToolNotFoundError(f"Cannot resolve version '{spec}' for {self.tool_name}")

        log.debug(f"Resolved {self.tool_name} version {spec} to {resolved}")
        return resolved

    def xǁBaseToolManagerǁresolve_version__mutmut_7(self, spec: str) -> str:
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

        resolved = self.resolver.resolve(available)
        if not resolved:
            raise ToolNotFoundError(f"Cannot resolve version '{spec}' for {self.tool_name}")

        log.debug(f"Resolved {self.tool_name} version {spec} to {resolved}")
        return resolved

    def xǁBaseToolManagerǁresolve_version__mutmut_8(self, spec: str) -> str:
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

        resolved = self.resolver.resolve(spec, )
        if not resolved:
            raise ToolNotFoundError(f"Cannot resolve version '{spec}' for {self.tool_name}")

        log.debug(f"Resolved {self.tool_name} version {spec} to {resolved}")
        return resolved

    def xǁBaseToolManagerǁresolve_version__mutmut_9(self, spec: str) -> str:
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
        if resolved:
            raise ToolNotFoundError(f"Cannot resolve version '{spec}' for {self.tool_name}")

        log.debug(f"Resolved {self.tool_name} version {spec} to {resolved}")
        return resolved

    def xǁBaseToolManagerǁresolve_version__mutmut_10(self, spec: str) -> str:
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
            raise ToolNotFoundError(None)

        log.debug(f"Resolved {self.tool_name} version {spec} to {resolved}")
        return resolved

    def xǁBaseToolManagerǁresolve_version__mutmut_11(self, spec: str) -> str:
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

        log.debug(None)
        return resolved
    
    xǁBaseToolManagerǁresolve_version__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolManagerǁresolve_version__mutmut_1': xǁBaseToolManagerǁresolve_version__mutmut_1, 
        'xǁBaseToolManagerǁresolve_version__mutmut_2': xǁBaseToolManagerǁresolve_version__mutmut_2, 
        'xǁBaseToolManagerǁresolve_version__mutmut_3': xǁBaseToolManagerǁresolve_version__mutmut_3, 
        'xǁBaseToolManagerǁresolve_version__mutmut_4': xǁBaseToolManagerǁresolve_version__mutmut_4, 
        'xǁBaseToolManagerǁresolve_version__mutmut_5': xǁBaseToolManagerǁresolve_version__mutmut_5, 
        'xǁBaseToolManagerǁresolve_version__mutmut_6': xǁBaseToolManagerǁresolve_version__mutmut_6, 
        'xǁBaseToolManagerǁresolve_version__mutmut_7': xǁBaseToolManagerǁresolve_version__mutmut_7, 
        'xǁBaseToolManagerǁresolve_version__mutmut_8': xǁBaseToolManagerǁresolve_version__mutmut_8, 
        'xǁBaseToolManagerǁresolve_version__mutmut_9': xǁBaseToolManagerǁresolve_version__mutmut_9, 
        'xǁBaseToolManagerǁresolve_version__mutmut_10': xǁBaseToolManagerǁresolve_version__mutmut_10, 
        'xǁBaseToolManagerǁresolve_version__mutmut_11': xǁBaseToolManagerǁresolve_version__mutmut_11
    }
    
    def resolve_version(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolManagerǁresolve_version__mutmut_orig"), object.__getattribute__(self, "xǁBaseToolManagerǁresolve_version__mutmut_mutants"), args, kwargs, self)
        return result 
    
    resolve_version.__signature__ = _mutmut_signature(xǁBaseToolManagerǁresolve_version__mutmut_orig)
    xǁBaseToolManagerǁresolve_version__mutmut_orig.__name__ = 'xǁBaseToolManagerǁresolve_version'

    async def xǁBaseToolManagerǁinstall__mutmut_orig(self, version: str = "latest", force: bool = False) -> Path:
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

    async def xǁBaseToolManagerǁinstall__mutmut_1(self, version: str = "XXlatestXX", force: bool = False) -> Path:
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

    async def xǁBaseToolManagerǁinstall__mutmut_2(self, version: str = "LATEST", force: bool = False) -> Path:
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

    async def xǁBaseToolManagerǁinstall__mutmut_3(self, version: str = "latest", force: bool = True) -> Path:
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

    async def xǁBaseToolManagerǁinstall__mutmut_4(self, version: str = "latest", force: bool = False) -> Path:
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
        if version in ["latest", "stable", "dev"] and version.startswith(("~", "^")):
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

    async def xǁBaseToolManagerǁinstall__mutmut_5(self, version: str = "latest", force: bool = False) -> Path:
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
        if version not in ["latest", "stable", "dev"] or version.startswith(("~", "^")):
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

    async def xǁBaseToolManagerǁinstall__mutmut_6(self, version: str = "latest", force: bool = False) -> Path:
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
        if version in ["XXlatestXX", "stable", "dev"] or version.startswith(("~", "^")):
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

    async def xǁBaseToolManagerǁinstall__mutmut_7(self, version: str = "latest", force: bool = False) -> Path:
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
        if version in ["LATEST", "stable", "dev"] or version.startswith(("~", "^")):
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

    async def xǁBaseToolManagerǁinstall__mutmut_8(self, version: str = "latest", force: bool = False) -> Path:
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
        if version in ["latest", "XXstableXX", "dev"] or version.startswith(("~", "^")):
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

    async def xǁBaseToolManagerǁinstall__mutmut_9(self, version: str = "latest", force: bool = False) -> Path:
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
        if version in ["latest", "STABLE", "dev"] or version.startswith(("~", "^")):
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

    async def xǁBaseToolManagerǁinstall__mutmut_10(self, version: str = "latest", force: bool = False) -> Path:
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
        if version in ["latest", "stable", "XXdevXX"] or version.startswith(("~", "^")):
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

    async def xǁBaseToolManagerǁinstall__mutmut_11(self, version: str = "latest", force: bool = False) -> Path:
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
        if version in ["latest", "stable", "DEV"] or version.startswith(("~", "^")):
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

    async def xǁBaseToolManagerǁinstall__mutmut_12(self, version: str = "latest", force: bool = False) -> Path:
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
        if version in ["latest", "stable", "dev"] or version.startswith(None):
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

    async def xǁBaseToolManagerǁinstall__mutmut_13(self, version: str = "latest", force: bool = False) -> Path:
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
        if version in ["latest", "stable", "dev"] or version.startswith(("XX~XX", "^")):
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

    async def xǁBaseToolManagerǁinstall__mutmut_14(self, version: str = "latest", force: bool = False) -> Path:
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
        if version in ["latest", "stable", "dev"] or version.startswith(("~", "XX^XX")):
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

    async def xǁBaseToolManagerǁinstall__mutmut_15(self, version: str = "latest", force: bool = False) -> Path:
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
            version = None

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

    async def xǁBaseToolManagerǁinstall__mutmut_16(self, version: str = "latest", force: bool = False) -> Path:
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
            version = self.resolve_version(None)

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

    async def xǁBaseToolManagerǁinstall__mutmut_17(self, version: str = "latest", force: bool = False) -> Path:
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
        if not force or (cached_path := self.cache.get(self.tool_name, version)):
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

    async def xǁBaseToolManagerǁinstall__mutmut_18(self, version: str = "latest", force: bool = False) -> Path:
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
        if force and (cached_path := self.cache.get(self.tool_name, version)):
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

    async def xǁBaseToolManagerǁinstall__mutmut_19(self, version: str = "latest", force: bool = False) -> Path:
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
        if not force and (cached_path := self.cache.get(None, version)):
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

    async def xǁBaseToolManagerǁinstall__mutmut_20(self, version: str = "latest", force: bool = False) -> Path:
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
        if not force and (cached_path := self.cache.get(self.tool_name, None)):
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

    async def xǁBaseToolManagerǁinstall__mutmut_21(self, version: str = "latest", force: bool = False) -> Path:
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
        if not force and (cached_path := self.cache.get(version)):
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

    async def xǁBaseToolManagerǁinstall__mutmut_22(self, version: str = "latest", force: bool = False) -> Path:
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
        if not force and (cached_path := self.cache.get(self.tool_name, )):
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

    async def xǁBaseToolManagerǁinstall__mutmut_23(self, version: str = "latest", force: bool = False) -> Path:
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
            log.info(None)
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

    async def xǁBaseToolManagerǁinstall__mutmut_24(self, version: str = "latest", force: bool = False) -> Path:
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

        log.info(None)

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

    async def xǁBaseToolManagerǁinstall__mutmut_25(self, version: str = "latest", force: bool = False) -> Path:
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
        metadata = None
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

    async def xǁBaseToolManagerǁinstall__mutmut_26(self, version: str = "latest", force: bool = False) -> Path:
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
        metadata = self.get_metadata(None)
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

    async def xǁBaseToolManagerǁinstall__mutmut_27(self, version: str = "latest", force: bool = False) -> Path:
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
        if metadata.download_url:
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

    async def xǁBaseToolManagerǁinstall__mutmut_28(self, version: str = "latest", force: bool = False) -> Path:
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
            raise ToolInstallError(None)

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

    async def xǁBaseToolManagerǁinstall__mutmut_29(self, version: str = "latest", force: bool = False) -> Path:
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

        download_path = None
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

    async def xǁBaseToolManagerǁinstall__mutmut_30(self, version: str = "latest", force: bool = False) -> Path:
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

        download_path = system_temp_dir() * f"{self.tool_name}-{version}"
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

    async def xǁBaseToolManagerǁinstall__mutmut_31(self, version: str = "latest", force: bool = False) -> Path:
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
        artifact_path = None

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

    async def xǁBaseToolManagerǁinstall__mutmut_32(self, version: str = "latest", force: bool = False) -> Path:
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
            None,
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

    async def xǁBaseToolManagerǁinstall__mutmut_33(self, version: str = "latest", force: bool = False) -> Path:
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
            None,
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

    async def xǁBaseToolManagerǁinstall__mutmut_34(self, version: str = "latest", force: bool = False) -> Path:
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
            None,
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

    async def xǁBaseToolManagerǁinstall__mutmut_35(self, version: str = "latest", force: bool = False) -> Path:
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

    async def xǁBaseToolManagerǁinstall__mutmut_36(self, version: str = "latest", force: bool = False) -> Path:
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

    async def xǁBaseToolManagerǁinstall__mutmut_37(self, version: str = "latest", force: bool = False) -> Path:
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

    async def xǁBaseToolManagerǁinstall__mutmut_38(self, version: str = "latest", force: bool = False) -> Path:
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
        if metadata.checksum or not self.verifier.verify_checksum(artifact_path, metadata.checksum):
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

    async def xǁBaseToolManagerǁinstall__mutmut_39(self, version: str = "latest", force: bool = False) -> Path:
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
        if metadata.checksum and self.verifier.verify_checksum(artifact_path, metadata.checksum):
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

    async def xǁBaseToolManagerǁinstall__mutmut_40(self, version: str = "latest", force: bool = False) -> Path:
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
        if metadata.checksum and not self.verifier.verify_checksum(None, metadata.checksum):
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

    async def xǁBaseToolManagerǁinstall__mutmut_41(self, version: str = "latest", force: bool = False) -> Path:
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
        if metadata.checksum and not self.verifier.verify_checksum(artifact_path, None):
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

    async def xǁBaseToolManagerǁinstall__mutmut_42(self, version: str = "latest", force: bool = False) -> Path:
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
        if metadata.checksum and not self.verifier.verify_checksum(metadata.checksum):
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

    async def xǁBaseToolManagerǁinstall__mutmut_43(self, version: str = "latest", force: bool = False) -> Path:
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
        if metadata.checksum and not self.verifier.verify_checksum(artifact_path, ):
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

    async def xǁBaseToolManagerǁinstall__mutmut_44(self, version: str = "latest", force: bool = False) -> Path:
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
            raise ToolVerificationError(None)

        # Install
        install_path = self.installer.install(artifact_path, metadata)

        # Cache the installation
        self.cache.store(self.tool_name, version, install_path)

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    async def xǁBaseToolManagerǁinstall__mutmut_45(self, version: str = "latest", force: bool = False) -> Path:
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
        install_path = None

        # Cache the installation
        self.cache.store(self.tool_name, version, install_path)

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    async def xǁBaseToolManagerǁinstall__mutmut_46(self, version: str = "latest", force: bool = False) -> Path:
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
        install_path = self.installer.install(None, metadata)

        # Cache the installation
        self.cache.store(self.tool_name, version, install_path)

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    async def xǁBaseToolManagerǁinstall__mutmut_47(self, version: str = "latest", force: bool = False) -> Path:
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
        install_path = self.installer.install(artifact_path, None)

        # Cache the installation
        self.cache.store(self.tool_name, version, install_path)

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    async def xǁBaseToolManagerǁinstall__mutmut_48(self, version: str = "latest", force: bool = False) -> Path:
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
        install_path = self.installer.install(metadata)

        # Cache the installation
        self.cache.store(self.tool_name, version, install_path)

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    async def xǁBaseToolManagerǁinstall__mutmut_49(self, version: str = "latest", force: bool = False) -> Path:
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
        install_path = self.installer.install(artifact_path, )

        # Cache the installation
        self.cache.store(self.tool_name, version, install_path)

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    async def xǁBaseToolManagerǁinstall__mutmut_50(self, version: str = "latest", force: bool = False) -> Path:
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
        self.cache.store(None, version, install_path)

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    async def xǁBaseToolManagerǁinstall__mutmut_51(self, version: str = "latest", force: bool = False) -> Path:
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
        self.cache.store(self.tool_name, None, install_path)

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    async def xǁBaseToolManagerǁinstall__mutmut_52(self, version: str = "latest", force: bool = False) -> Path:
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
        self.cache.store(self.tool_name, version, None)

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    async def xǁBaseToolManagerǁinstall__mutmut_53(self, version: str = "latest", force: bool = False) -> Path:
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
        self.cache.store(version, install_path)

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    async def xǁBaseToolManagerǁinstall__mutmut_54(self, version: str = "latest", force: bool = False) -> Path:
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
        self.cache.store(self.tool_name, install_path)

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    async def xǁBaseToolManagerǁinstall__mutmut_55(self, version: str = "latest", force: bool = False) -> Path:
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
        self.cache.store(self.tool_name, version, )

        # Clean up download
        if artifact_path.exists():
            artifact_path.unlink()

        log.info(f"Successfully installed {self.tool_name} {version} to {install_path}")
        return install_path

    async def xǁBaseToolManagerǁinstall__mutmut_56(self, version: str = "latest", force: bool = False) -> Path:
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

        log.info(None)
        return install_path
    
    xǁBaseToolManagerǁinstall__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolManagerǁinstall__mutmut_1': xǁBaseToolManagerǁinstall__mutmut_1, 
        'xǁBaseToolManagerǁinstall__mutmut_2': xǁBaseToolManagerǁinstall__mutmut_2, 
        'xǁBaseToolManagerǁinstall__mutmut_3': xǁBaseToolManagerǁinstall__mutmut_3, 
        'xǁBaseToolManagerǁinstall__mutmut_4': xǁBaseToolManagerǁinstall__mutmut_4, 
        'xǁBaseToolManagerǁinstall__mutmut_5': xǁBaseToolManagerǁinstall__mutmut_5, 
        'xǁBaseToolManagerǁinstall__mutmut_6': xǁBaseToolManagerǁinstall__mutmut_6, 
        'xǁBaseToolManagerǁinstall__mutmut_7': xǁBaseToolManagerǁinstall__mutmut_7, 
        'xǁBaseToolManagerǁinstall__mutmut_8': xǁBaseToolManagerǁinstall__mutmut_8, 
        'xǁBaseToolManagerǁinstall__mutmut_9': xǁBaseToolManagerǁinstall__mutmut_9, 
        'xǁBaseToolManagerǁinstall__mutmut_10': xǁBaseToolManagerǁinstall__mutmut_10, 
        'xǁBaseToolManagerǁinstall__mutmut_11': xǁBaseToolManagerǁinstall__mutmut_11, 
        'xǁBaseToolManagerǁinstall__mutmut_12': xǁBaseToolManagerǁinstall__mutmut_12, 
        'xǁBaseToolManagerǁinstall__mutmut_13': xǁBaseToolManagerǁinstall__mutmut_13, 
        'xǁBaseToolManagerǁinstall__mutmut_14': xǁBaseToolManagerǁinstall__mutmut_14, 
        'xǁBaseToolManagerǁinstall__mutmut_15': xǁBaseToolManagerǁinstall__mutmut_15, 
        'xǁBaseToolManagerǁinstall__mutmut_16': xǁBaseToolManagerǁinstall__mutmut_16, 
        'xǁBaseToolManagerǁinstall__mutmut_17': xǁBaseToolManagerǁinstall__mutmut_17, 
        'xǁBaseToolManagerǁinstall__mutmut_18': xǁBaseToolManagerǁinstall__mutmut_18, 
        'xǁBaseToolManagerǁinstall__mutmut_19': xǁBaseToolManagerǁinstall__mutmut_19, 
        'xǁBaseToolManagerǁinstall__mutmut_20': xǁBaseToolManagerǁinstall__mutmut_20, 
        'xǁBaseToolManagerǁinstall__mutmut_21': xǁBaseToolManagerǁinstall__mutmut_21, 
        'xǁBaseToolManagerǁinstall__mutmut_22': xǁBaseToolManagerǁinstall__mutmut_22, 
        'xǁBaseToolManagerǁinstall__mutmut_23': xǁBaseToolManagerǁinstall__mutmut_23, 
        'xǁBaseToolManagerǁinstall__mutmut_24': xǁBaseToolManagerǁinstall__mutmut_24, 
        'xǁBaseToolManagerǁinstall__mutmut_25': xǁBaseToolManagerǁinstall__mutmut_25, 
        'xǁBaseToolManagerǁinstall__mutmut_26': xǁBaseToolManagerǁinstall__mutmut_26, 
        'xǁBaseToolManagerǁinstall__mutmut_27': xǁBaseToolManagerǁinstall__mutmut_27, 
        'xǁBaseToolManagerǁinstall__mutmut_28': xǁBaseToolManagerǁinstall__mutmut_28, 
        'xǁBaseToolManagerǁinstall__mutmut_29': xǁBaseToolManagerǁinstall__mutmut_29, 
        'xǁBaseToolManagerǁinstall__mutmut_30': xǁBaseToolManagerǁinstall__mutmut_30, 
        'xǁBaseToolManagerǁinstall__mutmut_31': xǁBaseToolManagerǁinstall__mutmut_31, 
        'xǁBaseToolManagerǁinstall__mutmut_32': xǁBaseToolManagerǁinstall__mutmut_32, 
        'xǁBaseToolManagerǁinstall__mutmut_33': xǁBaseToolManagerǁinstall__mutmut_33, 
        'xǁBaseToolManagerǁinstall__mutmut_34': xǁBaseToolManagerǁinstall__mutmut_34, 
        'xǁBaseToolManagerǁinstall__mutmut_35': xǁBaseToolManagerǁinstall__mutmut_35, 
        'xǁBaseToolManagerǁinstall__mutmut_36': xǁBaseToolManagerǁinstall__mutmut_36, 
        'xǁBaseToolManagerǁinstall__mutmut_37': xǁBaseToolManagerǁinstall__mutmut_37, 
        'xǁBaseToolManagerǁinstall__mutmut_38': xǁBaseToolManagerǁinstall__mutmut_38, 
        'xǁBaseToolManagerǁinstall__mutmut_39': xǁBaseToolManagerǁinstall__mutmut_39, 
        'xǁBaseToolManagerǁinstall__mutmut_40': xǁBaseToolManagerǁinstall__mutmut_40, 
        'xǁBaseToolManagerǁinstall__mutmut_41': xǁBaseToolManagerǁinstall__mutmut_41, 
        'xǁBaseToolManagerǁinstall__mutmut_42': xǁBaseToolManagerǁinstall__mutmut_42, 
        'xǁBaseToolManagerǁinstall__mutmut_43': xǁBaseToolManagerǁinstall__mutmut_43, 
        'xǁBaseToolManagerǁinstall__mutmut_44': xǁBaseToolManagerǁinstall__mutmut_44, 
        'xǁBaseToolManagerǁinstall__mutmut_45': xǁBaseToolManagerǁinstall__mutmut_45, 
        'xǁBaseToolManagerǁinstall__mutmut_46': xǁBaseToolManagerǁinstall__mutmut_46, 
        'xǁBaseToolManagerǁinstall__mutmut_47': xǁBaseToolManagerǁinstall__mutmut_47, 
        'xǁBaseToolManagerǁinstall__mutmut_48': xǁBaseToolManagerǁinstall__mutmut_48, 
        'xǁBaseToolManagerǁinstall__mutmut_49': xǁBaseToolManagerǁinstall__mutmut_49, 
        'xǁBaseToolManagerǁinstall__mutmut_50': xǁBaseToolManagerǁinstall__mutmut_50, 
        'xǁBaseToolManagerǁinstall__mutmut_51': xǁBaseToolManagerǁinstall__mutmut_51, 
        'xǁBaseToolManagerǁinstall__mutmut_52': xǁBaseToolManagerǁinstall__mutmut_52, 
        'xǁBaseToolManagerǁinstall__mutmut_53': xǁBaseToolManagerǁinstall__mutmut_53, 
        'xǁBaseToolManagerǁinstall__mutmut_54': xǁBaseToolManagerǁinstall__mutmut_54, 
        'xǁBaseToolManagerǁinstall__mutmut_55': xǁBaseToolManagerǁinstall__mutmut_55, 
        'xǁBaseToolManagerǁinstall__mutmut_56': xǁBaseToolManagerǁinstall__mutmut_56
    }
    
    def install(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolManagerǁinstall__mutmut_orig"), object.__getattribute__(self, "xǁBaseToolManagerǁinstall__mutmut_mutants"), args, kwargs, self)
        return result 
    
    install.__signature__ = _mutmut_signature(xǁBaseToolManagerǁinstall__mutmut_orig)
    xǁBaseToolManagerǁinstall__mutmut_orig.__name__ = 'xǁBaseToolManagerǁinstall'

    def xǁBaseToolManagerǁuninstall__mutmut_orig(self, version: str) -> bool:
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

    def xǁBaseToolManagerǁuninstall__mutmut_1(self, version: str) -> bool:
        """Uninstall a specific version.

        Args:
            version: Version to uninstall.

        Returns:
            True if uninstalled, False if not found.

        """
        # Invalidate cache
        self.cache.invalidate(None, version)

        # Remove from filesystem
        install_path = self.get_install_path(version)
        if install_path.exists():
            import shutil

            shutil.rmtree(install_path)
            log.info(f"Uninstalled {self.tool_name} {version}")
            return True

        return False

    def xǁBaseToolManagerǁuninstall__mutmut_2(self, version: str) -> bool:
        """Uninstall a specific version.

        Args:
            version: Version to uninstall.

        Returns:
            True if uninstalled, False if not found.

        """
        # Invalidate cache
        self.cache.invalidate(self.tool_name, None)

        # Remove from filesystem
        install_path = self.get_install_path(version)
        if install_path.exists():
            import shutil

            shutil.rmtree(install_path)
            log.info(f"Uninstalled {self.tool_name} {version}")
            return True

        return False

    def xǁBaseToolManagerǁuninstall__mutmut_3(self, version: str) -> bool:
        """Uninstall a specific version.

        Args:
            version: Version to uninstall.

        Returns:
            True if uninstalled, False if not found.

        """
        # Invalidate cache
        self.cache.invalidate(version)

        # Remove from filesystem
        install_path = self.get_install_path(version)
        if install_path.exists():
            import shutil

            shutil.rmtree(install_path)
            log.info(f"Uninstalled {self.tool_name} {version}")
            return True

        return False

    def xǁBaseToolManagerǁuninstall__mutmut_4(self, version: str) -> bool:
        """Uninstall a specific version.

        Args:
            version: Version to uninstall.

        Returns:
            True if uninstalled, False if not found.

        """
        # Invalidate cache
        self.cache.invalidate(self.tool_name, )

        # Remove from filesystem
        install_path = self.get_install_path(version)
        if install_path.exists():
            import shutil

            shutil.rmtree(install_path)
            log.info(f"Uninstalled {self.tool_name} {version}")
            return True

        return False

    def xǁBaseToolManagerǁuninstall__mutmut_5(self, version: str) -> bool:
        """Uninstall a specific version.

        Args:
            version: Version to uninstall.

        Returns:
            True if uninstalled, False if not found.

        """
        # Invalidate cache
        self.cache.invalidate(self.tool_name, version)

        # Remove from filesystem
        install_path = None
        if install_path.exists():
            import shutil

            shutil.rmtree(install_path)
            log.info(f"Uninstalled {self.tool_name} {version}")
            return True

        return False

    def xǁBaseToolManagerǁuninstall__mutmut_6(self, version: str) -> bool:
        """Uninstall a specific version.

        Args:
            version: Version to uninstall.

        Returns:
            True if uninstalled, False if not found.

        """
        # Invalidate cache
        self.cache.invalidate(self.tool_name, version)

        # Remove from filesystem
        install_path = self.get_install_path(None)
        if install_path.exists():
            import shutil

            shutil.rmtree(install_path)
            log.info(f"Uninstalled {self.tool_name} {version}")
            return True

        return False

    def xǁBaseToolManagerǁuninstall__mutmut_7(self, version: str) -> bool:
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

            shutil.rmtree(None)
            log.info(f"Uninstalled {self.tool_name} {version}")
            return True

        return False

    def xǁBaseToolManagerǁuninstall__mutmut_8(self, version: str) -> bool:
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
            log.info(None)
            return True

        return False

    def xǁBaseToolManagerǁuninstall__mutmut_9(self, version: str) -> bool:
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
            return False

        return False

    def xǁBaseToolManagerǁuninstall__mutmut_10(self, version: str) -> bool:
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

        return True
    
    xǁBaseToolManagerǁuninstall__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolManagerǁuninstall__mutmut_1': xǁBaseToolManagerǁuninstall__mutmut_1, 
        'xǁBaseToolManagerǁuninstall__mutmut_2': xǁBaseToolManagerǁuninstall__mutmut_2, 
        'xǁBaseToolManagerǁuninstall__mutmut_3': xǁBaseToolManagerǁuninstall__mutmut_3, 
        'xǁBaseToolManagerǁuninstall__mutmut_4': xǁBaseToolManagerǁuninstall__mutmut_4, 
        'xǁBaseToolManagerǁuninstall__mutmut_5': xǁBaseToolManagerǁuninstall__mutmut_5, 
        'xǁBaseToolManagerǁuninstall__mutmut_6': xǁBaseToolManagerǁuninstall__mutmut_6, 
        'xǁBaseToolManagerǁuninstall__mutmut_7': xǁBaseToolManagerǁuninstall__mutmut_7, 
        'xǁBaseToolManagerǁuninstall__mutmut_8': xǁBaseToolManagerǁuninstall__mutmut_8, 
        'xǁBaseToolManagerǁuninstall__mutmut_9': xǁBaseToolManagerǁuninstall__mutmut_9, 
        'xǁBaseToolManagerǁuninstall__mutmut_10': xǁBaseToolManagerǁuninstall__mutmut_10
    }
    
    def uninstall(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolManagerǁuninstall__mutmut_orig"), object.__getattribute__(self, "xǁBaseToolManagerǁuninstall__mutmut_mutants"), args, kwargs, self)
        return result 
    
    uninstall.__signature__ = _mutmut_signature(xǁBaseToolManagerǁuninstall__mutmut_orig)
    xǁBaseToolManagerǁuninstall__mutmut_orig.__name__ = 'xǁBaseToolManagerǁuninstall'

    def xǁBaseToolManagerǁget_install_path__mutmut_orig(self, version: str) -> Path:
        """Get the installation path for a version.

        Args:
            version: Version string.

        Returns:
            Path where the version is/will be installed.

        """
        base_path = Path.home() / ".provide-foundation" / "tools" / self.tool_name / version
        return base_path

    def xǁBaseToolManagerǁget_install_path__mutmut_1(self, version: str) -> Path:
        """Get the installation path for a version.

        Args:
            version: Version string.

        Returns:
            Path where the version is/will be installed.

        """
        base_path = None
        return base_path

    def xǁBaseToolManagerǁget_install_path__mutmut_2(self, version: str) -> Path:
        """Get the installation path for a version.

        Args:
            version: Version string.

        Returns:
            Path where the version is/will be installed.

        """
        base_path = Path.home() / ".provide-foundation" / "tools" / self.tool_name * version
        return base_path

    def xǁBaseToolManagerǁget_install_path__mutmut_3(self, version: str) -> Path:
        """Get the installation path for a version.

        Args:
            version: Version string.

        Returns:
            Path where the version is/will be installed.

        """
        base_path = Path.home() / ".provide-foundation" / "tools" * self.tool_name / version
        return base_path

    def xǁBaseToolManagerǁget_install_path__mutmut_4(self, version: str) -> Path:
        """Get the installation path for a version.

        Args:
            version: Version string.

        Returns:
            Path where the version is/will be installed.

        """
        base_path = Path.home() / ".provide-foundation" * "tools" / self.tool_name / version
        return base_path

    def xǁBaseToolManagerǁget_install_path__mutmut_5(self, version: str) -> Path:
        """Get the installation path for a version.

        Args:
            version: Version string.

        Returns:
            Path where the version is/will be installed.

        """
        base_path = Path.home() * ".provide-foundation" / "tools" / self.tool_name / version
        return base_path

    def xǁBaseToolManagerǁget_install_path__mutmut_6(self, version: str) -> Path:
        """Get the installation path for a version.

        Args:
            version: Version string.

        Returns:
            Path where the version is/will be installed.

        """
        base_path = Path.home() / "XX.provide-foundationXX" / "tools" / self.tool_name / version
        return base_path

    def xǁBaseToolManagerǁget_install_path__mutmut_7(self, version: str) -> Path:
        """Get the installation path for a version.

        Args:
            version: Version string.

        Returns:
            Path where the version is/will be installed.

        """
        base_path = Path.home() / ".PROVIDE-FOUNDATION" / "tools" / self.tool_name / version
        return base_path

    def xǁBaseToolManagerǁget_install_path__mutmut_8(self, version: str) -> Path:
        """Get the installation path for a version.

        Args:
            version: Version string.

        Returns:
            Path where the version is/will be installed.

        """
        base_path = Path.home() / ".provide-foundation" / "XXtoolsXX" / self.tool_name / version
        return base_path

    def xǁBaseToolManagerǁget_install_path__mutmut_9(self, version: str) -> Path:
        """Get the installation path for a version.

        Args:
            version: Version string.

        Returns:
            Path where the version is/will be installed.

        """
        base_path = Path.home() / ".provide-foundation" / "TOOLS" / self.tool_name / version
        return base_path
    
    xǁBaseToolManagerǁget_install_path__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolManagerǁget_install_path__mutmut_1': xǁBaseToolManagerǁget_install_path__mutmut_1, 
        'xǁBaseToolManagerǁget_install_path__mutmut_2': xǁBaseToolManagerǁget_install_path__mutmut_2, 
        'xǁBaseToolManagerǁget_install_path__mutmut_3': xǁBaseToolManagerǁget_install_path__mutmut_3, 
        'xǁBaseToolManagerǁget_install_path__mutmut_4': xǁBaseToolManagerǁget_install_path__mutmut_4, 
        'xǁBaseToolManagerǁget_install_path__mutmut_5': xǁBaseToolManagerǁget_install_path__mutmut_5, 
        'xǁBaseToolManagerǁget_install_path__mutmut_6': xǁBaseToolManagerǁget_install_path__mutmut_6, 
        'xǁBaseToolManagerǁget_install_path__mutmut_7': xǁBaseToolManagerǁget_install_path__mutmut_7, 
        'xǁBaseToolManagerǁget_install_path__mutmut_8': xǁBaseToolManagerǁget_install_path__mutmut_8, 
        'xǁBaseToolManagerǁget_install_path__mutmut_9': xǁBaseToolManagerǁget_install_path__mutmut_9
    }
    
    def get_install_path(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolManagerǁget_install_path__mutmut_orig"), object.__getattribute__(self, "xǁBaseToolManagerǁget_install_path__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_install_path.__signature__ = _mutmut_signature(xǁBaseToolManagerǁget_install_path__mutmut_orig)
    xǁBaseToolManagerǁget_install_path__mutmut_orig.__name__ = 'xǁBaseToolManagerǁget_install_path'

    def xǁBaseToolManagerǁis_installed__mutmut_orig(self, version: str) -> bool:
        """Check if a version is installed.

        Args:
            version: Version to check.

        Returns:
            True if installed, False otherwise.

        """
        install_path = self.get_install_path(version)
        executable = install_path / "bin" / self.executable_name
        return executable.exists()

    def xǁBaseToolManagerǁis_installed__mutmut_1(self, version: str) -> bool:
        """Check if a version is installed.

        Args:
            version: Version to check.

        Returns:
            True if installed, False otherwise.

        """
        install_path = None
        executable = install_path / "bin" / self.executable_name
        return executable.exists()

    def xǁBaseToolManagerǁis_installed__mutmut_2(self, version: str) -> bool:
        """Check if a version is installed.

        Args:
            version: Version to check.

        Returns:
            True if installed, False otherwise.

        """
        install_path = self.get_install_path(None)
        executable = install_path / "bin" / self.executable_name
        return executable.exists()

    def xǁBaseToolManagerǁis_installed__mutmut_3(self, version: str) -> bool:
        """Check if a version is installed.

        Args:
            version: Version to check.

        Returns:
            True if installed, False otherwise.

        """
        install_path = self.get_install_path(version)
        executable = None
        return executable.exists()

    def xǁBaseToolManagerǁis_installed__mutmut_4(self, version: str) -> bool:
        """Check if a version is installed.

        Args:
            version: Version to check.

        Returns:
            True if installed, False otherwise.

        """
        install_path = self.get_install_path(version)
        executable = install_path / "bin" * self.executable_name
        return executable.exists()

    def xǁBaseToolManagerǁis_installed__mutmut_5(self, version: str) -> bool:
        """Check if a version is installed.

        Args:
            version: Version to check.

        Returns:
            True if installed, False otherwise.

        """
        install_path = self.get_install_path(version)
        executable = install_path * "bin" / self.executable_name
        return executable.exists()

    def xǁBaseToolManagerǁis_installed__mutmut_6(self, version: str) -> bool:
        """Check if a version is installed.

        Args:
            version: Version to check.

        Returns:
            True if installed, False otherwise.

        """
        install_path = self.get_install_path(version)
        executable = install_path / "XXbinXX" / self.executable_name
        return executable.exists()

    def xǁBaseToolManagerǁis_installed__mutmut_7(self, version: str) -> bool:
        """Check if a version is installed.

        Args:
            version: Version to check.

        Returns:
            True if installed, False otherwise.

        """
        install_path = self.get_install_path(version)
        executable = install_path / "BIN" / self.executable_name
        return executable.exists()
    
    xǁBaseToolManagerǁis_installed__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolManagerǁis_installed__mutmut_1': xǁBaseToolManagerǁis_installed__mutmut_1, 
        'xǁBaseToolManagerǁis_installed__mutmut_2': xǁBaseToolManagerǁis_installed__mutmut_2, 
        'xǁBaseToolManagerǁis_installed__mutmut_3': xǁBaseToolManagerǁis_installed__mutmut_3, 
        'xǁBaseToolManagerǁis_installed__mutmut_4': xǁBaseToolManagerǁis_installed__mutmut_4, 
        'xǁBaseToolManagerǁis_installed__mutmut_5': xǁBaseToolManagerǁis_installed__mutmut_5, 
        'xǁBaseToolManagerǁis_installed__mutmut_6': xǁBaseToolManagerǁis_installed__mutmut_6, 
        'xǁBaseToolManagerǁis_installed__mutmut_7': xǁBaseToolManagerǁis_installed__mutmut_7
    }
    
    def is_installed(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolManagerǁis_installed__mutmut_orig"), object.__getattribute__(self, "xǁBaseToolManagerǁis_installed__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_installed.__signature__ = _mutmut_signature(xǁBaseToolManagerǁis_installed__mutmut_orig)
    xǁBaseToolManagerǁis_installed__mutmut_orig.__name__ = 'xǁBaseToolManagerǁis_installed'

    def xǁBaseToolManagerǁget_platform_info__mutmut_orig(self) -> dict[str, str]:
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_1(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = None
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_2(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().upper()
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_3(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system != "darwin":
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_4(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system == "XXdarwinXX":
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_5(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system == "DARWIN":
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_6(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system == "darwin":
            system = None
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_7(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system == "darwin":
            system = "XXdarwinXX"
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_8(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system == "darwin":
            system = "DARWIN"
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_9(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system == "darwin":
            system = "darwin"
        elif system != "linux":
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_10(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system == "darwin":
            system = "darwin"
        elif system == "XXlinuxXX":
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_11(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system == "darwin":
            system = "darwin"
        elif system == "LINUX":
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_12(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system == "darwin":
            system = "darwin"
        elif system == "linux":
            system = None
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_13(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system == "darwin":
            system = "darwin"
        elif system == "linux":
            system = "XXlinuxXX"
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_14(self) -> dict[str, str]:
        """Get current platform information.

        Returns:
            Dictionary with platform and arch keys.

        """
        import platform

        system = platform.system().lower()
        if system == "darwin":
            system = "darwin"
        elif system == "linux":
            system = "LINUX"
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

    def xǁBaseToolManagerǁget_platform_info__mutmut_15(self) -> dict[str, str]:
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
        elif system != "windows":
            system = "windows"

        machine = platform.machine().lower()
        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_16(self) -> dict[str, str]:
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
        elif system == "XXwindowsXX":
            system = "windows"

        machine = platform.machine().lower()
        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_17(self) -> dict[str, str]:
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
        elif system == "WINDOWS":
            system = "windows"

        machine = platform.machine().lower()
        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_18(self) -> dict[str, str]:
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
            system = None

        machine = platform.machine().lower()
        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_19(self) -> dict[str, str]:
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
            system = "XXwindowsXX"

        machine = platform.machine().lower()
        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_20(self) -> dict[str, str]:
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
            system = "WINDOWS"

        machine = platform.machine().lower()
        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_21(self) -> dict[str, str]:
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

        machine = None
        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_22(self) -> dict[str, str]:
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

        machine = platform.machine().upper()
        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_23(self) -> dict[str, str]:
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
        if machine not in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_24(self) -> dict[str, str]:
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
        if machine in ["XXx86_64XX", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_25(self) -> dict[str, str]:
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
        if machine in ["X86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_26(self) -> dict[str, str]:
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
        if machine in ["x86_64", "XXamd64XX"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_27(self) -> dict[str, str]:
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
        if machine in ["x86_64", "AMD64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_28(self) -> dict[str, str]:
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
            arch = None
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_29(self) -> dict[str, str]:
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
            arch = "XXamd64XX"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_30(self) -> dict[str, str]:
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
            arch = "AMD64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_31(self) -> dict[str, str]:
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
        elif machine not in ["aarch64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_32(self) -> dict[str, str]:
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
        elif machine in ["XXaarch64XX", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_33(self) -> dict[str, str]:
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
        elif machine in ["AARCH64", "arm64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_34(self) -> dict[str, str]:
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
        elif machine in ["aarch64", "XXarm64XX"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_35(self) -> dict[str, str]:
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
        elif machine in ["aarch64", "ARM64"]:
            arch = "arm64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_36(self) -> dict[str, str]:
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
            arch = None
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_37(self) -> dict[str, str]:
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
            arch = "XXarm64XX"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_38(self) -> dict[str, str]:
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
            arch = "ARM64"
        else:
            arch = machine

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_39(self) -> dict[str, str]:
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
            arch = None

        return {"platform": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_40(self) -> dict[str, str]:
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

        return {"XXplatformXX": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_41(self) -> dict[str, str]:
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

        return {"PLATFORM": system, "arch": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_42(self) -> dict[str, str]:
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

        return {"platform": system, "XXarchXX": arch}

    def xǁBaseToolManagerǁget_platform_info__mutmut_43(self) -> dict[str, str]:
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

        return {"platform": system, "ARCH": arch}
    
    xǁBaseToolManagerǁget_platform_info__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolManagerǁget_platform_info__mutmut_1': xǁBaseToolManagerǁget_platform_info__mutmut_1, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_2': xǁBaseToolManagerǁget_platform_info__mutmut_2, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_3': xǁBaseToolManagerǁget_platform_info__mutmut_3, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_4': xǁBaseToolManagerǁget_platform_info__mutmut_4, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_5': xǁBaseToolManagerǁget_platform_info__mutmut_5, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_6': xǁBaseToolManagerǁget_platform_info__mutmut_6, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_7': xǁBaseToolManagerǁget_platform_info__mutmut_7, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_8': xǁBaseToolManagerǁget_platform_info__mutmut_8, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_9': xǁBaseToolManagerǁget_platform_info__mutmut_9, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_10': xǁBaseToolManagerǁget_platform_info__mutmut_10, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_11': xǁBaseToolManagerǁget_platform_info__mutmut_11, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_12': xǁBaseToolManagerǁget_platform_info__mutmut_12, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_13': xǁBaseToolManagerǁget_platform_info__mutmut_13, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_14': xǁBaseToolManagerǁget_platform_info__mutmut_14, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_15': xǁBaseToolManagerǁget_platform_info__mutmut_15, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_16': xǁBaseToolManagerǁget_platform_info__mutmut_16, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_17': xǁBaseToolManagerǁget_platform_info__mutmut_17, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_18': xǁBaseToolManagerǁget_platform_info__mutmut_18, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_19': xǁBaseToolManagerǁget_platform_info__mutmut_19, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_20': xǁBaseToolManagerǁget_platform_info__mutmut_20, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_21': xǁBaseToolManagerǁget_platform_info__mutmut_21, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_22': xǁBaseToolManagerǁget_platform_info__mutmut_22, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_23': xǁBaseToolManagerǁget_platform_info__mutmut_23, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_24': xǁBaseToolManagerǁget_platform_info__mutmut_24, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_25': xǁBaseToolManagerǁget_platform_info__mutmut_25, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_26': xǁBaseToolManagerǁget_platform_info__mutmut_26, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_27': xǁBaseToolManagerǁget_platform_info__mutmut_27, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_28': xǁBaseToolManagerǁget_platform_info__mutmut_28, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_29': xǁBaseToolManagerǁget_platform_info__mutmut_29, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_30': xǁBaseToolManagerǁget_platform_info__mutmut_30, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_31': xǁBaseToolManagerǁget_platform_info__mutmut_31, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_32': xǁBaseToolManagerǁget_platform_info__mutmut_32, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_33': xǁBaseToolManagerǁget_platform_info__mutmut_33, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_34': xǁBaseToolManagerǁget_platform_info__mutmut_34, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_35': xǁBaseToolManagerǁget_platform_info__mutmut_35, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_36': xǁBaseToolManagerǁget_platform_info__mutmut_36, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_37': xǁBaseToolManagerǁget_platform_info__mutmut_37, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_38': xǁBaseToolManagerǁget_platform_info__mutmut_38, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_39': xǁBaseToolManagerǁget_platform_info__mutmut_39, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_40': xǁBaseToolManagerǁget_platform_info__mutmut_40, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_41': xǁBaseToolManagerǁget_platform_info__mutmut_41, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_42': xǁBaseToolManagerǁget_platform_info__mutmut_42, 
        'xǁBaseToolManagerǁget_platform_info__mutmut_43': xǁBaseToolManagerǁget_platform_info__mutmut_43
    }
    
    def get_platform_info(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolManagerǁget_platform_info__mutmut_orig"), object.__getattribute__(self, "xǁBaseToolManagerǁget_platform_info__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_platform_info.__signature__ = _mutmut_signature(xǁBaseToolManagerǁget_platform_info__mutmut_orig)
    xǁBaseToolManagerǁget_platform_info__mutmut_orig.__name__ = 'xǁBaseToolManagerǁget_platform_info'


# <3 🧱🤝🔧🪄
