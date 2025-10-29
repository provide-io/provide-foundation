# provide/foundation/tools/installer.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path
import shutil
import tarfile
import zipfile

from provide.foundation.errors import FoundationError
from provide.foundation.logger import get_logger
from provide.foundation.tools.base import ToolMetadata

"""Tool installation manager for various archive formats.

Handles extraction and installation of tools from different
archive formats (zip, tar, gz, etc.) and binary files.
"""

log = get_logger(__name__)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class InstallError(FoundationError):
    """Raised when installation fails."""


class ToolInstaller:
    """Handle tool installation from various artifact formats.

    Supports:
    - ZIP archives
    - TAR archives (with compression)
    - Single binary files
    - Platform-specific installation patterns
    """

    def xǁToolInstallerǁinstall__mutmut_orig(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_1(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_2(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(None)

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_3(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = None

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_4(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(None)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_5(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(None)

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_6(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = None
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_7(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.upper()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_8(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix != ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_9(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == "XX.zipXX":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_10(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".ZIP":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_11(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(None, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_12(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, None)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_13(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_14(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(
                artifact,
            )
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_15(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix not in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_16(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in ["XX.tarXX", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_17(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".TAR", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_18(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", "XX.gzXX", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_19(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".GZ", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_20(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", "XX.tgzXX", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_21(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".TGZ", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_22(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", "XX.bz2XX", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_23(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".BZ2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_24(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", "XX.xzXX"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_25(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".XZ"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_26(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(None, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_27(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, None)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_28(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_29(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(
                artifact,
            )
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_30(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(None):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_31(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(None, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_32(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, None, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_33(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, None)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_34(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_35(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_36(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(
                artifact,
                install_dir,
            )
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_37(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(None)

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_38(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(None, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_39(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, None)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_40(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_41(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(
            install_dir,
        )

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_42(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(None, metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_43(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, None)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_44(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(metadata)

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_45(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(
            install_dir,
        )

        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir

    def xǁToolInstallerǁinstall__mutmut_46(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """Install tool from artifact.

        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.

        Returns:
            Path to installed tool directory.

        Raises:
            InstallError: If installation fails.

        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")

        # Determine install directory
        install_dir = self.get_install_dir(metadata)

        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")

        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")

        # Set permissions
        self.set_permissions(install_dir, metadata)

        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)

        log.info(None)
        return install_dir

    xǁToolInstallerǁinstall__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolInstallerǁinstall__mutmut_1": xǁToolInstallerǁinstall__mutmut_1,
        "xǁToolInstallerǁinstall__mutmut_2": xǁToolInstallerǁinstall__mutmut_2,
        "xǁToolInstallerǁinstall__mutmut_3": xǁToolInstallerǁinstall__mutmut_3,
        "xǁToolInstallerǁinstall__mutmut_4": xǁToolInstallerǁinstall__mutmut_4,
        "xǁToolInstallerǁinstall__mutmut_5": xǁToolInstallerǁinstall__mutmut_5,
        "xǁToolInstallerǁinstall__mutmut_6": xǁToolInstallerǁinstall__mutmut_6,
        "xǁToolInstallerǁinstall__mutmut_7": xǁToolInstallerǁinstall__mutmut_7,
        "xǁToolInstallerǁinstall__mutmut_8": xǁToolInstallerǁinstall__mutmut_8,
        "xǁToolInstallerǁinstall__mutmut_9": xǁToolInstallerǁinstall__mutmut_9,
        "xǁToolInstallerǁinstall__mutmut_10": xǁToolInstallerǁinstall__mutmut_10,
        "xǁToolInstallerǁinstall__mutmut_11": xǁToolInstallerǁinstall__mutmut_11,
        "xǁToolInstallerǁinstall__mutmut_12": xǁToolInstallerǁinstall__mutmut_12,
        "xǁToolInstallerǁinstall__mutmut_13": xǁToolInstallerǁinstall__mutmut_13,
        "xǁToolInstallerǁinstall__mutmut_14": xǁToolInstallerǁinstall__mutmut_14,
        "xǁToolInstallerǁinstall__mutmut_15": xǁToolInstallerǁinstall__mutmut_15,
        "xǁToolInstallerǁinstall__mutmut_16": xǁToolInstallerǁinstall__mutmut_16,
        "xǁToolInstallerǁinstall__mutmut_17": xǁToolInstallerǁinstall__mutmut_17,
        "xǁToolInstallerǁinstall__mutmut_18": xǁToolInstallerǁinstall__mutmut_18,
        "xǁToolInstallerǁinstall__mutmut_19": xǁToolInstallerǁinstall__mutmut_19,
        "xǁToolInstallerǁinstall__mutmut_20": xǁToolInstallerǁinstall__mutmut_20,
        "xǁToolInstallerǁinstall__mutmut_21": xǁToolInstallerǁinstall__mutmut_21,
        "xǁToolInstallerǁinstall__mutmut_22": xǁToolInstallerǁinstall__mutmut_22,
        "xǁToolInstallerǁinstall__mutmut_23": xǁToolInstallerǁinstall__mutmut_23,
        "xǁToolInstallerǁinstall__mutmut_24": xǁToolInstallerǁinstall__mutmut_24,
        "xǁToolInstallerǁinstall__mutmut_25": xǁToolInstallerǁinstall__mutmut_25,
        "xǁToolInstallerǁinstall__mutmut_26": xǁToolInstallerǁinstall__mutmut_26,
        "xǁToolInstallerǁinstall__mutmut_27": xǁToolInstallerǁinstall__mutmut_27,
        "xǁToolInstallerǁinstall__mutmut_28": xǁToolInstallerǁinstall__mutmut_28,
        "xǁToolInstallerǁinstall__mutmut_29": xǁToolInstallerǁinstall__mutmut_29,
        "xǁToolInstallerǁinstall__mutmut_30": xǁToolInstallerǁinstall__mutmut_30,
        "xǁToolInstallerǁinstall__mutmut_31": xǁToolInstallerǁinstall__mutmut_31,
        "xǁToolInstallerǁinstall__mutmut_32": xǁToolInstallerǁinstall__mutmut_32,
        "xǁToolInstallerǁinstall__mutmut_33": xǁToolInstallerǁinstall__mutmut_33,
        "xǁToolInstallerǁinstall__mutmut_34": xǁToolInstallerǁinstall__mutmut_34,
        "xǁToolInstallerǁinstall__mutmut_35": xǁToolInstallerǁinstall__mutmut_35,
        "xǁToolInstallerǁinstall__mutmut_36": xǁToolInstallerǁinstall__mutmut_36,
        "xǁToolInstallerǁinstall__mutmut_37": xǁToolInstallerǁinstall__mutmut_37,
        "xǁToolInstallerǁinstall__mutmut_38": xǁToolInstallerǁinstall__mutmut_38,
        "xǁToolInstallerǁinstall__mutmut_39": xǁToolInstallerǁinstall__mutmut_39,
        "xǁToolInstallerǁinstall__mutmut_40": xǁToolInstallerǁinstall__mutmut_40,
        "xǁToolInstallerǁinstall__mutmut_41": xǁToolInstallerǁinstall__mutmut_41,
        "xǁToolInstallerǁinstall__mutmut_42": xǁToolInstallerǁinstall__mutmut_42,
        "xǁToolInstallerǁinstall__mutmut_43": xǁToolInstallerǁinstall__mutmut_43,
        "xǁToolInstallerǁinstall__mutmut_44": xǁToolInstallerǁinstall__mutmut_44,
        "xǁToolInstallerǁinstall__mutmut_45": xǁToolInstallerǁinstall__mutmut_45,
        "xǁToolInstallerǁinstall__mutmut_46": xǁToolInstallerǁinstall__mutmut_46,
    }

    def install(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolInstallerǁinstall__mutmut_orig"),
            object.__getattribute__(self, "xǁToolInstallerǁinstall__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    install.__signature__ = _mutmut_signature(xǁToolInstallerǁinstall__mutmut_orig)
    xǁToolInstallerǁinstall__mutmut_orig.__name__ = "xǁToolInstallerǁinstall"

    def xǁToolInstallerǁget_install_dir__mutmut_orig(self, metadata: ToolMetadata) -> Path:
        """Get installation directory for tool.

        Args:
            metadata: Tool metadata.

        Returns:
            Installation directory path.

        """
        if metadata.install_path:
            return metadata.install_path

        # Default to ~/.provide-foundation/tools/<name>/<version>
        base = Path.home() / ".provide-foundation" / "tools"
        return base / metadata.name / metadata.version

    def xǁToolInstallerǁget_install_dir__mutmut_1(self, metadata: ToolMetadata) -> Path:
        """Get installation directory for tool.

        Args:
            metadata: Tool metadata.

        Returns:
            Installation directory path.

        """
        if metadata.install_path:
            return metadata.install_path

        # Default to ~/.provide-foundation/tools/<name>/<version>
        base = None
        return base / metadata.name / metadata.version

    def xǁToolInstallerǁget_install_dir__mutmut_2(self, metadata: ToolMetadata) -> Path:
        """Get installation directory for tool.

        Args:
            metadata: Tool metadata.

        Returns:
            Installation directory path.

        """
        if metadata.install_path:
            return metadata.install_path

        # Default to ~/.provide-foundation/tools/<name>/<version>
        base = Path.home() / ".provide-foundation" * "tools"
        return base / metadata.name / metadata.version

    def xǁToolInstallerǁget_install_dir__mutmut_3(self, metadata: ToolMetadata) -> Path:
        """Get installation directory for tool.

        Args:
            metadata: Tool metadata.

        Returns:
            Installation directory path.

        """
        if metadata.install_path:
            return metadata.install_path

        # Default to ~/.provide-foundation/tools/<name>/<version>
        base = Path.home() * ".provide-foundation" / "tools"
        return base / metadata.name / metadata.version

    def xǁToolInstallerǁget_install_dir__mutmut_4(self, metadata: ToolMetadata) -> Path:
        """Get installation directory for tool.

        Args:
            metadata: Tool metadata.

        Returns:
            Installation directory path.

        """
        if metadata.install_path:
            return metadata.install_path

        # Default to ~/.provide-foundation/tools/<name>/<version>
        base = Path.home() / "XX.provide-foundationXX" / "tools"
        return base / metadata.name / metadata.version

    def xǁToolInstallerǁget_install_dir__mutmut_5(self, metadata: ToolMetadata) -> Path:
        """Get installation directory for tool.

        Args:
            metadata: Tool metadata.

        Returns:
            Installation directory path.

        """
        if metadata.install_path:
            return metadata.install_path

        # Default to ~/.provide-foundation/tools/<name>/<version>
        base = Path.home() / ".PROVIDE-FOUNDATION" / "tools"
        return base / metadata.name / metadata.version

    def xǁToolInstallerǁget_install_dir__mutmut_6(self, metadata: ToolMetadata) -> Path:
        """Get installation directory for tool.

        Args:
            metadata: Tool metadata.

        Returns:
            Installation directory path.

        """
        if metadata.install_path:
            return metadata.install_path

        # Default to ~/.provide-foundation/tools/<name>/<version>
        base = Path.home() / ".provide-foundation" / "XXtoolsXX"
        return base / metadata.name / metadata.version

    def xǁToolInstallerǁget_install_dir__mutmut_7(self, metadata: ToolMetadata) -> Path:
        """Get installation directory for tool.

        Args:
            metadata: Tool metadata.

        Returns:
            Installation directory path.

        """
        if metadata.install_path:
            return metadata.install_path

        # Default to ~/.provide-foundation/tools/<name>/<version>
        base = Path.home() / ".provide-foundation" / "TOOLS"
        return base / metadata.name / metadata.version

    def xǁToolInstallerǁget_install_dir__mutmut_8(self, metadata: ToolMetadata) -> Path:
        """Get installation directory for tool.

        Args:
            metadata: Tool metadata.

        Returns:
            Installation directory path.

        """
        if metadata.install_path:
            return metadata.install_path

        # Default to ~/.provide-foundation/tools/<name>/<version>
        base = Path.home() / ".provide-foundation" / "tools"
        return base / metadata.name * metadata.version

    def xǁToolInstallerǁget_install_dir__mutmut_9(self, metadata: ToolMetadata) -> Path:
        """Get installation directory for tool.

        Args:
            metadata: Tool metadata.

        Returns:
            Installation directory path.

        """
        if metadata.install_path:
            return metadata.install_path

        # Default to ~/.provide-foundation/tools/<name>/<version>
        base = Path.home() / ".provide-foundation" / "tools"
        return base * metadata.name / metadata.version

    xǁToolInstallerǁget_install_dir__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolInstallerǁget_install_dir__mutmut_1": xǁToolInstallerǁget_install_dir__mutmut_1,
        "xǁToolInstallerǁget_install_dir__mutmut_2": xǁToolInstallerǁget_install_dir__mutmut_2,
        "xǁToolInstallerǁget_install_dir__mutmut_3": xǁToolInstallerǁget_install_dir__mutmut_3,
        "xǁToolInstallerǁget_install_dir__mutmut_4": xǁToolInstallerǁget_install_dir__mutmut_4,
        "xǁToolInstallerǁget_install_dir__mutmut_5": xǁToolInstallerǁget_install_dir__mutmut_5,
        "xǁToolInstallerǁget_install_dir__mutmut_6": xǁToolInstallerǁget_install_dir__mutmut_6,
        "xǁToolInstallerǁget_install_dir__mutmut_7": xǁToolInstallerǁget_install_dir__mutmut_7,
        "xǁToolInstallerǁget_install_dir__mutmut_8": xǁToolInstallerǁget_install_dir__mutmut_8,
        "xǁToolInstallerǁget_install_dir__mutmut_9": xǁToolInstallerǁget_install_dir__mutmut_9,
    }

    def get_install_dir(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolInstallerǁget_install_dir__mutmut_orig"),
            object.__getattribute__(self, "xǁToolInstallerǁget_install_dir__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_install_dir.__signature__ = _mutmut_signature(xǁToolInstallerǁget_install_dir__mutmut_orig)
    xǁToolInstallerǁget_install_dir__mutmut_orig.__name__ = "xǁToolInstallerǁget_install_dir"

    def xǁToolInstallerǁextract_zip__mutmut_orig(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_1(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(None)

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_2(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=None, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_3(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=None)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_4(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_5(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(
            parents=True,
        )

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_6(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=False, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_7(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=False)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_8(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(None, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_9(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, None) as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_10(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile("r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_11(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(
            archive,
        ) as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_12(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "XXrXX") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_13(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "R") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_14(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = None
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_15(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") and ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_16(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith(None) or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_17(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("XX/XX") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_18(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or "XX..XX" in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_19(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." not in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_20(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(None)

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_21(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = None
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_22(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) * member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_23(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(None) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_24(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(None)
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_25(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(None) from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_26(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(None)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_27(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(None, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_28(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(dest, members=None)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_29(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_zip__mutmut_30(self, archive: Path, dest: Path) -> None:
        """Extract ZIP archive.

        Args:
            archive: Path to ZIP file.
            dest: Destination directory.

        """
        log.debug(f"Extracting ZIP {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths and validate members
            safe_members = []
            for member_name in zf.namelist():
                if member_name.startswith("/") or ".." in member_name:
                    raise InstallError(f"Unsafe path in archive: {member_name}")

                # Additional security check for path traversal
                member_path = Path(dest) / member_name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member_name}") from None

                safe_members.append(member_name)

            # Extract only validated members (all members have been security-checked above)
            zf.extractall(
                dest,
            )  # nosec B202

    xǁToolInstallerǁextract_zip__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolInstallerǁextract_zip__mutmut_1": xǁToolInstallerǁextract_zip__mutmut_1,
        "xǁToolInstallerǁextract_zip__mutmut_2": xǁToolInstallerǁextract_zip__mutmut_2,
        "xǁToolInstallerǁextract_zip__mutmut_3": xǁToolInstallerǁextract_zip__mutmut_3,
        "xǁToolInstallerǁextract_zip__mutmut_4": xǁToolInstallerǁextract_zip__mutmut_4,
        "xǁToolInstallerǁextract_zip__mutmut_5": xǁToolInstallerǁextract_zip__mutmut_5,
        "xǁToolInstallerǁextract_zip__mutmut_6": xǁToolInstallerǁextract_zip__mutmut_6,
        "xǁToolInstallerǁextract_zip__mutmut_7": xǁToolInstallerǁextract_zip__mutmut_7,
        "xǁToolInstallerǁextract_zip__mutmut_8": xǁToolInstallerǁextract_zip__mutmut_8,
        "xǁToolInstallerǁextract_zip__mutmut_9": xǁToolInstallerǁextract_zip__mutmut_9,
        "xǁToolInstallerǁextract_zip__mutmut_10": xǁToolInstallerǁextract_zip__mutmut_10,
        "xǁToolInstallerǁextract_zip__mutmut_11": xǁToolInstallerǁextract_zip__mutmut_11,
        "xǁToolInstallerǁextract_zip__mutmut_12": xǁToolInstallerǁextract_zip__mutmut_12,
        "xǁToolInstallerǁextract_zip__mutmut_13": xǁToolInstallerǁextract_zip__mutmut_13,
        "xǁToolInstallerǁextract_zip__mutmut_14": xǁToolInstallerǁextract_zip__mutmut_14,
        "xǁToolInstallerǁextract_zip__mutmut_15": xǁToolInstallerǁextract_zip__mutmut_15,
        "xǁToolInstallerǁextract_zip__mutmut_16": xǁToolInstallerǁextract_zip__mutmut_16,
        "xǁToolInstallerǁextract_zip__mutmut_17": xǁToolInstallerǁextract_zip__mutmut_17,
        "xǁToolInstallerǁextract_zip__mutmut_18": xǁToolInstallerǁextract_zip__mutmut_18,
        "xǁToolInstallerǁextract_zip__mutmut_19": xǁToolInstallerǁextract_zip__mutmut_19,
        "xǁToolInstallerǁextract_zip__mutmut_20": xǁToolInstallerǁextract_zip__mutmut_20,
        "xǁToolInstallerǁextract_zip__mutmut_21": xǁToolInstallerǁextract_zip__mutmut_21,
        "xǁToolInstallerǁextract_zip__mutmut_22": xǁToolInstallerǁextract_zip__mutmut_22,
        "xǁToolInstallerǁextract_zip__mutmut_23": xǁToolInstallerǁextract_zip__mutmut_23,
        "xǁToolInstallerǁextract_zip__mutmut_24": xǁToolInstallerǁextract_zip__mutmut_24,
        "xǁToolInstallerǁextract_zip__mutmut_25": xǁToolInstallerǁextract_zip__mutmut_25,
        "xǁToolInstallerǁextract_zip__mutmut_26": xǁToolInstallerǁextract_zip__mutmut_26,
        "xǁToolInstallerǁextract_zip__mutmut_27": xǁToolInstallerǁextract_zip__mutmut_27,
        "xǁToolInstallerǁextract_zip__mutmut_28": xǁToolInstallerǁextract_zip__mutmut_28,
        "xǁToolInstallerǁextract_zip__mutmut_29": xǁToolInstallerǁextract_zip__mutmut_29,
        "xǁToolInstallerǁextract_zip__mutmut_30": xǁToolInstallerǁextract_zip__mutmut_30,
    }

    def extract_zip(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolInstallerǁextract_zip__mutmut_orig"),
            object.__getattribute__(self, "xǁToolInstallerǁextract_zip__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    extract_zip.__signature__ = _mutmut_signature(xǁToolInstallerǁextract_zip__mutmut_orig)
    xǁToolInstallerǁextract_zip__mutmut_orig.__name__ = "xǁToolInstallerǁextract_zip"

    def xǁToolInstallerǁextract_tar__mutmut_orig(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_1(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(None)

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_2(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=None, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_3(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=None)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_4(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_5(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(
            parents=True,
        )

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_6(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=False, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_7(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=False)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_8(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = None
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_9(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "XXrXX"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_10(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "R"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_11(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix not in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_12(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in ["XX.gzXX", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_13(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".GZ", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_14(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", "XX.tgzXX"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_15(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".TGZ"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_16(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = None
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_17(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "XXr:gzXX"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_18(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "R:GZ"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_19(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix != ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_20(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == "XX.bz2XX":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_21(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".BZ2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_22(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = None
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_23(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "XXr:bz2XX"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_24(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "R:BZ2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_25(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix != ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_26(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == "XX.xzXX":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_27(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".XZ":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_28(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = None

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_29(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "XXr:xzXX"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_30(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "R:XZ"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_31(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(None, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_32(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, None) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_33(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_34(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(
            archive,
        ) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_35(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = None
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_36(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") and ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_37(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith(None) or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_38(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("XX/XX") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_39(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or "XX..XX" in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_40(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." not in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_41(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(None)

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_42(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() and member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_43(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = None
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_44(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) * member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_45(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(None) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_46(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = None
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_47(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(None)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_48(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_49(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = None
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_50(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent * target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_51(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(None)
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_52(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(None).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_53(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(None) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_54(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = None
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_55(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) * member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_56(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(None) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_57(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(None)
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_58(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(None) from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_59(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(None)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_60(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(None, members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_61(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(dest, members=None)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_62(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(members=safe_members)  # nosec B202

    def xǁToolInstallerǁextract_tar__mutmut_63(self, archive: Path, dest: Path) -> None:
        """Extract tar archive (with optional compression).

        Args:
            archive: Path to tar file.
            dest: Destination directory.

        """
        log.debug(f"Extracting tar {archive} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)

        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"

        with tarfile.open(archive, mode) as tf:  # type: ignore[call-overload]
            # Check for unsafe paths and validate members
            safe_members = []
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")

                # Additional security checks for symlinks
                if member.islnk() or member.issym():
                    # Check that symlinks don't escape extraction directory
                    link_path = Path(dest) / member.name
                    target = Path(member.linkname)
                    if not target.is_absolute():
                        target = link_path.parent / target
                    try:
                        target.resolve().relative_to(Path(dest).resolve())
                    except ValueError:
                        raise InstallError(
                            f"Unsafe symlink in archive: {member.name} -> {member.linkname}"
                        ) from None

                # Path traversal check
                member_path = Path(dest) / member.name
                try:
                    member_path.resolve().relative_to(dest.resolve())
                except ValueError:
                    raise InstallError(f"Path traversal detected in archive: {member.name}") from None

                safe_members.append(member)

            # Extract only validated members (all members have been security-checked above)
            tf.extractall(
                dest,
            )  # nosec B202

    xǁToolInstallerǁextract_tar__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolInstallerǁextract_tar__mutmut_1": xǁToolInstallerǁextract_tar__mutmut_1,
        "xǁToolInstallerǁextract_tar__mutmut_2": xǁToolInstallerǁextract_tar__mutmut_2,
        "xǁToolInstallerǁextract_tar__mutmut_3": xǁToolInstallerǁextract_tar__mutmut_3,
        "xǁToolInstallerǁextract_tar__mutmut_4": xǁToolInstallerǁextract_tar__mutmut_4,
        "xǁToolInstallerǁextract_tar__mutmut_5": xǁToolInstallerǁextract_tar__mutmut_5,
        "xǁToolInstallerǁextract_tar__mutmut_6": xǁToolInstallerǁextract_tar__mutmut_6,
        "xǁToolInstallerǁextract_tar__mutmut_7": xǁToolInstallerǁextract_tar__mutmut_7,
        "xǁToolInstallerǁextract_tar__mutmut_8": xǁToolInstallerǁextract_tar__mutmut_8,
        "xǁToolInstallerǁextract_tar__mutmut_9": xǁToolInstallerǁextract_tar__mutmut_9,
        "xǁToolInstallerǁextract_tar__mutmut_10": xǁToolInstallerǁextract_tar__mutmut_10,
        "xǁToolInstallerǁextract_tar__mutmut_11": xǁToolInstallerǁextract_tar__mutmut_11,
        "xǁToolInstallerǁextract_tar__mutmut_12": xǁToolInstallerǁextract_tar__mutmut_12,
        "xǁToolInstallerǁextract_tar__mutmut_13": xǁToolInstallerǁextract_tar__mutmut_13,
        "xǁToolInstallerǁextract_tar__mutmut_14": xǁToolInstallerǁextract_tar__mutmut_14,
        "xǁToolInstallerǁextract_tar__mutmut_15": xǁToolInstallerǁextract_tar__mutmut_15,
        "xǁToolInstallerǁextract_tar__mutmut_16": xǁToolInstallerǁextract_tar__mutmut_16,
        "xǁToolInstallerǁextract_tar__mutmut_17": xǁToolInstallerǁextract_tar__mutmut_17,
        "xǁToolInstallerǁextract_tar__mutmut_18": xǁToolInstallerǁextract_tar__mutmut_18,
        "xǁToolInstallerǁextract_tar__mutmut_19": xǁToolInstallerǁextract_tar__mutmut_19,
        "xǁToolInstallerǁextract_tar__mutmut_20": xǁToolInstallerǁextract_tar__mutmut_20,
        "xǁToolInstallerǁextract_tar__mutmut_21": xǁToolInstallerǁextract_tar__mutmut_21,
        "xǁToolInstallerǁextract_tar__mutmut_22": xǁToolInstallerǁextract_tar__mutmut_22,
        "xǁToolInstallerǁextract_tar__mutmut_23": xǁToolInstallerǁextract_tar__mutmut_23,
        "xǁToolInstallerǁextract_tar__mutmut_24": xǁToolInstallerǁextract_tar__mutmut_24,
        "xǁToolInstallerǁextract_tar__mutmut_25": xǁToolInstallerǁextract_tar__mutmut_25,
        "xǁToolInstallerǁextract_tar__mutmut_26": xǁToolInstallerǁextract_tar__mutmut_26,
        "xǁToolInstallerǁextract_tar__mutmut_27": xǁToolInstallerǁextract_tar__mutmut_27,
        "xǁToolInstallerǁextract_tar__mutmut_28": xǁToolInstallerǁextract_tar__mutmut_28,
        "xǁToolInstallerǁextract_tar__mutmut_29": xǁToolInstallerǁextract_tar__mutmut_29,
        "xǁToolInstallerǁextract_tar__mutmut_30": xǁToolInstallerǁextract_tar__mutmut_30,
        "xǁToolInstallerǁextract_tar__mutmut_31": xǁToolInstallerǁextract_tar__mutmut_31,
        "xǁToolInstallerǁextract_tar__mutmut_32": xǁToolInstallerǁextract_tar__mutmut_32,
        "xǁToolInstallerǁextract_tar__mutmut_33": xǁToolInstallerǁextract_tar__mutmut_33,
        "xǁToolInstallerǁextract_tar__mutmut_34": xǁToolInstallerǁextract_tar__mutmut_34,
        "xǁToolInstallerǁextract_tar__mutmut_35": xǁToolInstallerǁextract_tar__mutmut_35,
        "xǁToolInstallerǁextract_tar__mutmut_36": xǁToolInstallerǁextract_tar__mutmut_36,
        "xǁToolInstallerǁextract_tar__mutmut_37": xǁToolInstallerǁextract_tar__mutmut_37,
        "xǁToolInstallerǁextract_tar__mutmut_38": xǁToolInstallerǁextract_tar__mutmut_38,
        "xǁToolInstallerǁextract_tar__mutmut_39": xǁToolInstallerǁextract_tar__mutmut_39,
        "xǁToolInstallerǁextract_tar__mutmut_40": xǁToolInstallerǁextract_tar__mutmut_40,
        "xǁToolInstallerǁextract_tar__mutmut_41": xǁToolInstallerǁextract_tar__mutmut_41,
        "xǁToolInstallerǁextract_tar__mutmut_42": xǁToolInstallerǁextract_tar__mutmut_42,
        "xǁToolInstallerǁextract_tar__mutmut_43": xǁToolInstallerǁextract_tar__mutmut_43,
        "xǁToolInstallerǁextract_tar__mutmut_44": xǁToolInstallerǁextract_tar__mutmut_44,
        "xǁToolInstallerǁextract_tar__mutmut_45": xǁToolInstallerǁextract_tar__mutmut_45,
        "xǁToolInstallerǁextract_tar__mutmut_46": xǁToolInstallerǁextract_tar__mutmut_46,
        "xǁToolInstallerǁextract_tar__mutmut_47": xǁToolInstallerǁextract_tar__mutmut_47,
        "xǁToolInstallerǁextract_tar__mutmut_48": xǁToolInstallerǁextract_tar__mutmut_48,
        "xǁToolInstallerǁextract_tar__mutmut_49": xǁToolInstallerǁextract_tar__mutmut_49,
        "xǁToolInstallerǁextract_tar__mutmut_50": xǁToolInstallerǁextract_tar__mutmut_50,
        "xǁToolInstallerǁextract_tar__mutmut_51": xǁToolInstallerǁextract_tar__mutmut_51,
        "xǁToolInstallerǁextract_tar__mutmut_52": xǁToolInstallerǁextract_tar__mutmut_52,
        "xǁToolInstallerǁextract_tar__mutmut_53": xǁToolInstallerǁextract_tar__mutmut_53,
        "xǁToolInstallerǁextract_tar__mutmut_54": xǁToolInstallerǁextract_tar__mutmut_54,
        "xǁToolInstallerǁextract_tar__mutmut_55": xǁToolInstallerǁextract_tar__mutmut_55,
        "xǁToolInstallerǁextract_tar__mutmut_56": xǁToolInstallerǁextract_tar__mutmut_56,
        "xǁToolInstallerǁextract_tar__mutmut_57": xǁToolInstallerǁextract_tar__mutmut_57,
        "xǁToolInstallerǁextract_tar__mutmut_58": xǁToolInstallerǁextract_tar__mutmut_58,
        "xǁToolInstallerǁextract_tar__mutmut_59": xǁToolInstallerǁextract_tar__mutmut_59,
        "xǁToolInstallerǁextract_tar__mutmut_60": xǁToolInstallerǁextract_tar__mutmut_60,
        "xǁToolInstallerǁextract_tar__mutmut_61": xǁToolInstallerǁextract_tar__mutmut_61,
        "xǁToolInstallerǁextract_tar__mutmut_62": xǁToolInstallerǁextract_tar__mutmut_62,
        "xǁToolInstallerǁextract_tar__mutmut_63": xǁToolInstallerǁextract_tar__mutmut_63,
    }

    def extract_tar(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolInstallerǁextract_tar__mutmut_orig"),
            object.__getattribute__(self, "xǁToolInstallerǁextract_tar__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    extract_tar.__signature__ = _mutmut_signature(xǁToolInstallerǁextract_tar__mutmut_orig)
    xǁToolInstallerǁextract_tar__mutmut_orig.__name__ = "xǁToolInstallerǁextract_tar"

    def xǁToolInstallerǁis_binary__mutmut_orig(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_1(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix and file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_2(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_3(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix not in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_4(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in ["XX.exeXX", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_5(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".EXE", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_6(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", "XX.binXX"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_7(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".BIN"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_8(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open(None) as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_9(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("XXrbXX") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_10(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("RB") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_11(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = None
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_12(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(None)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_13(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(5)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_14(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(None):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_15(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"XX\x7fELFXX"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_16(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7felf"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_17(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_18(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return False
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_19(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(None):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_20(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"XXMZXX"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_21(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"mz"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_22(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_23(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return False
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_24(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(None):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_25(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"XX\xfe\xed\xfaXX"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_26(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_27(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_28(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return False
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_29(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(None):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_30(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"XX\xca\xfe\xba\xbeXX"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_31(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_32(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_33(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return False
            except Exception:
                pass

        return False

    def xǁToolInstallerǁis_binary__mutmut_34(self, file_path: Path) -> bool:
        """Check if file is a binary executable.

        Args:
            file_path: Path to check.

        Returns:
            True if file appears to be binary.

        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass

        return True

    xǁToolInstallerǁis_binary__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolInstallerǁis_binary__mutmut_1": xǁToolInstallerǁis_binary__mutmut_1,
        "xǁToolInstallerǁis_binary__mutmut_2": xǁToolInstallerǁis_binary__mutmut_2,
        "xǁToolInstallerǁis_binary__mutmut_3": xǁToolInstallerǁis_binary__mutmut_3,
        "xǁToolInstallerǁis_binary__mutmut_4": xǁToolInstallerǁis_binary__mutmut_4,
        "xǁToolInstallerǁis_binary__mutmut_5": xǁToolInstallerǁis_binary__mutmut_5,
        "xǁToolInstallerǁis_binary__mutmut_6": xǁToolInstallerǁis_binary__mutmut_6,
        "xǁToolInstallerǁis_binary__mutmut_7": xǁToolInstallerǁis_binary__mutmut_7,
        "xǁToolInstallerǁis_binary__mutmut_8": xǁToolInstallerǁis_binary__mutmut_8,
        "xǁToolInstallerǁis_binary__mutmut_9": xǁToolInstallerǁis_binary__mutmut_9,
        "xǁToolInstallerǁis_binary__mutmut_10": xǁToolInstallerǁis_binary__mutmut_10,
        "xǁToolInstallerǁis_binary__mutmut_11": xǁToolInstallerǁis_binary__mutmut_11,
        "xǁToolInstallerǁis_binary__mutmut_12": xǁToolInstallerǁis_binary__mutmut_12,
        "xǁToolInstallerǁis_binary__mutmut_13": xǁToolInstallerǁis_binary__mutmut_13,
        "xǁToolInstallerǁis_binary__mutmut_14": xǁToolInstallerǁis_binary__mutmut_14,
        "xǁToolInstallerǁis_binary__mutmut_15": xǁToolInstallerǁis_binary__mutmut_15,
        "xǁToolInstallerǁis_binary__mutmut_16": xǁToolInstallerǁis_binary__mutmut_16,
        "xǁToolInstallerǁis_binary__mutmut_17": xǁToolInstallerǁis_binary__mutmut_17,
        "xǁToolInstallerǁis_binary__mutmut_18": xǁToolInstallerǁis_binary__mutmut_18,
        "xǁToolInstallerǁis_binary__mutmut_19": xǁToolInstallerǁis_binary__mutmut_19,
        "xǁToolInstallerǁis_binary__mutmut_20": xǁToolInstallerǁis_binary__mutmut_20,
        "xǁToolInstallerǁis_binary__mutmut_21": xǁToolInstallerǁis_binary__mutmut_21,
        "xǁToolInstallerǁis_binary__mutmut_22": xǁToolInstallerǁis_binary__mutmut_22,
        "xǁToolInstallerǁis_binary__mutmut_23": xǁToolInstallerǁis_binary__mutmut_23,
        "xǁToolInstallerǁis_binary__mutmut_24": xǁToolInstallerǁis_binary__mutmut_24,
        "xǁToolInstallerǁis_binary__mutmut_25": xǁToolInstallerǁis_binary__mutmut_25,
        "xǁToolInstallerǁis_binary__mutmut_26": xǁToolInstallerǁis_binary__mutmut_26,
        "xǁToolInstallerǁis_binary__mutmut_27": xǁToolInstallerǁis_binary__mutmut_27,
        "xǁToolInstallerǁis_binary__mutmut_28": xǁToolInstallerǁis_binary__mutmut_28,
        "xǁToolInstallerǁis_binary__mutmut_29": xǁToolInstallerǁis_binary__mutmut_29,
        "xǁToolInstallerǁis_binary__mutmut_30": xǁToolInstallerǁis_binary__mutmut_30,
        "xǁToolInstallerǁis_binary__mutmut_31": xǁToolInstallerǁis_binary__mutmut_31,
        "xǁToolInstallerǁis_binary__mutmut_32": xǁToolInstallerǁis_binary__mutmut_32,
        "xǁToolInstallerǁis_binary__mutmut_33": xǁToolInstallerǁis_binary__mutmut_33,
        "xǁToolInstallerǁis_binary__mutmut_34": xǁToolInstallerǁis_binary__mutmut_34,
    }

    def is_binary(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolInstallerǁis_binary__mutmut_orig"),
            object.__getattribute__(self, "xǁToolInstallerǁis_binary__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    is_binary.__signature__ = _mutmut_signature(xǁToolInstallerǁis_binary__mutmut_orig)
    xǁToolInstallerǁis_binary__mutmut_orig.__name__ = "xǁToolInstallerǁis_binary"

    def xǁToolInstallerǁinstall_binary__mutmut_orig(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_1(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(None)

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_2(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=None, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_3(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=None)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_4(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_5(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(
            parents=True,
        )
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_6(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=False, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_7(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=False)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_8(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = None
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_9(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest * "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_10(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "XXbinXX"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_11(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "BIN"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_12(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=None)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_13(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=False)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_14(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = None
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_15(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name and binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_16(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = None

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_17(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir * target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_18(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(None, target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_19(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, None)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_20(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(target)

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_21(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(
            binary,
        )

        # Make executable
        target.chmod(0o755)

    def xǁToolInstallerǁinstall_binary__mutmut_22(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(None)

    def xǁToolInstallerǁinstall_binary__mutmut_23(
        self, binary: Path, dest: Path, metadata: ToolMetadata
    ) -> None:
        """Install single binary file.

        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.

        """
        log.debug(f"Installing binary {binary} to {dest}")

        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)

        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name

        # Copy binary
        shutil.copy2(binary, target)

        # Make executable
        target.chmod(494)

    xǁToolInstallerǁinstall_binary__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolInstallerǁinstall_binary__mutmut_1": xǁToolInstallerǁinstall_binary__mutmut_1,
        "xǁToolInstallerǁinstall_binary__mutmut_2": xǁToolInstallerǁinstall_binary__mutmut_2,
        "xǁToolInstallerǁinstall_binary__mutmut_3": xǁToolInstallerǁinstall_binary__mutmut_3,
        "xǁToolInstallerǁinstall_binary__mutmut_4": xǁToolInstallerǁinstall_binary__mutmut_4,
        "xǁToolInstallerǁinstall_binary__mutmut_5": xǁToolInstallerǁinstall_binary__mutmut_5,
        "xǁToolInstallerǁinstall_binary__mutmut_6": xǁToolInstallerǁinstall_binary__mutmut_6,
        "xǁToolInstallerǁinstall_binary__mutmut_7": xǁToolInstallerǁinstall_binary__mutmut_7,
        "xǁToolInstallerǁinstall_binary__mutmut_8": xǁToolInstallerǁinstall_binary__mutmut_8,
        "xǁToolInstallerǁinstall_binary__mutmut_9": xǁToolInstallerǁinstall_binary__mutmut_9,
        "xǁToolInstallerǁinstall_binary__mutmut_10": xǁToolInstallerǁinstall_binary__mutmut_10,
        "xǁToolInstallerǁinstall_binary__mutmut_11": xǁToolInstallerǁinstall_binary__mutmut_11,
        "xǁToolInstallerǁinstall_binary__mutmut_12": xǁToolInstallerǁinstall_binary__mutmut_12,
        "xǁToolInstallerǁinstall_binary__mutmut_13": xǁToolInstallerǁinstall_binary__mutmut_13,
        "xǁToolInstallerǁinstall_binary__mutmut_14": xǁToolInstallerǁinstall_binary__mutmut_14,
        "xǁToolInstallerǁinstall_binary__mutmut_15": xǁToolInstallerǁinstall_binary__mutmut_15,
        "xǁToolInstallerǁinstall_binary__mutmut_16": xǁToolInstallerǁinstall_binary__mutmut_16,
        "xǁToolInstallerǁinstall_binary__mutmut_17": xǁToolInstallerǁinstall_binary__mutmut_17,
        "xǁToolInstallerǁinstall_binary__mutmut_18": xǁToolInstallerǁinstall_binary__mutmut_18,
        "xǁToolInstallerǁinstall_binary__mutmut_19": xǁToolInstallerǁinstall_binary__mutmut_19,
        "xǁToolInstallerǁinstall_binary__mutmut_20": xǁToolInstallerǁinstall_binary__mutmut_20,
        "xǁToolInstallerǁinstall_binary__mutmut_21": xǁToolInstallerǁinstall_binary__mutmut_21,
        "xǁToolInstallerǁinstall_binary__mutmut_22": xǁToolInstallerǁinstall_binary__mutmut_22,
        "xǁToolInstallerǁinstall_binary__mutmut_23": xǁToolInstallerǁinstall_binary__mutmut_23,
    }

    def install_binary(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolInstallerǁinstall_binary__mutmut_orig"),
            object.__getattribute__(self, "xǁToolInstallerǁinstall_binary__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    install_binary.__signature__ = _mutmut_signature(xǁToolInstallerǁinstall_binary__mutmut_orig)
    xǁToolInstallerǁinstall_binary__mutmut_orig.__name__ = "xǁToolInstallerǁinstall_binary"

    def xǁToolInstallerǁset_permissions__mutmut_orig(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_1(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() != "Windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_2(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "XXWindowsXX":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_3(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_4(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "WINDOWS":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_5(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = None
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_6(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir * "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_7(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "XXbinXX"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_8(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "BIN"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_9(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(None)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_10(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(494)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_11(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = None
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_12(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir * metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)

    def xǁToolInstallerǁset_permissions__mutmut_13(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(None)

    def xǁToolInstallerǁset_permissions__mutmut_14(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Set appropriate permissions on installed files.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows handles permissions differently

        # Find executables and make them executable
        bin_dir = install_dir / "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)

        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(494)

    xǁToolInstallerǁset_permissions__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolInstallerǁset_permissions__mutmut_1": xǁToolInstallerǁset_permissions__mutmut_1,
        "xǁToolInstallerǁset_permissions__mutmut_2": xǁToolInstallerǁset_permissions__mutmut_2,
        "xǁToolInstallerǁset_permissions__mutmut_3": xǁToolInstallerǁset_permissions__mutmut_3,
        "xǁToolInstallerǁset_permissions__mutmut_4": xǁToolInstallerǁset_permissions__mutmut_4,
        "xǁToolInstallerǁset_permissions__mutmut_5": xǁToolInstallerǁset_permissions__mutmut_5,
        "xǁToolInstallerǁset_permissions__mutmut_6": xǁToolInstallerǁset_permissions__mutmut_6,
        "xǁToolInstallerǁset_permissions__mutmut_7": xǁToolInstallerǁset_permissions__mutmut_7,
        "xǁToolInstallerǁset_permissions__mutmut_8": xǁToolInstallerǁset_permissions__mutmut_8,
        "xǁToolInstallerǁset_permissions__mutmut_9": xǁToolInstallerǁset_permissions__mutmut_9,
        "xǁToolInstallerǁset_permissions__mutmut_10": xǁToolInstallerǁset_permissions__mutmut_10,
        "xǁToolInstallerǁset_permissions__mutmut_11": xǁToolInstallerǁset_permissions__mutmut_11,
        "xǁToolInstallerǁset_permissions__mutmut_12": xǁToolInstallerǁset_permissions__mutmut_12,
        "xǁToolInstallerǁset_permissions__mutmut_13": xǁToolInstallerǁset_permissions__mutmut_13,
        "xǁToolInstallerǁset_permissions__mutmut_14": xǁToolInstallerǁset_permissions__mutmut_14,
    }

    def set_permissions(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolInstallerǁset_permissions__mutmut_orig"),
            object.__getattribute__(self, "xǁToolInstallerǁset_permissions__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    set_permissions.__signature__ = _mutmut_signature(xǁToolInstallerǁset_permissions__mutmut_orig)
    xǁToolInstallerǁset_permissions__mutmut_orig.__name__ = "xǁToolInstallerǁset_permissions"

    def xǁToolInstallerǁcreate_symlinks__mutmut_orig(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = parent / "latest"

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_1(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() != "Windows":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = parent / "latest"

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_2(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "XXWindowsXX":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = parent / "latest"

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_3(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "windows":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = parent / "latest"

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_4(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "WINDOWS":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = parent / "latest"

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_5(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name or metadata.version:
            parent = install_dir.parent
            latest_link = parent / "latest"

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_6(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = None
            latest_link = parent / "latest"

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_7(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = None

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_8(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = parent * "latest"

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_9(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = parent / "XXlatestXX"

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_10(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = parent / "LATEST"

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_11(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = parent / "latest"

            if latest_link.exists() and latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_12(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = parent / "latest"

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(None)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")

    def xǁToolInstallerǁcreate_symlinks__mutmut_13(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """Create symlinks for easier access.

        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.

        """
        import platform

        if platform.system() == "Windows":
            return  # Windows doesn't support symlinks easily

        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = parent / "latest"

            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()

            latest_link.symlink_to(install_dir)
            log.debug(None)

    xǁToolInstallerǁcreate_symlinks__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁToolInstallerǁcreate_symlinks__mutmut_1": xǁToolInstallerǁcreate_symlinks__mutmut_1,
        "xǁToolInstallerǁcreate_symlinks__mutmut_2": xǁToolInstallerǁcreate_symlinks__mutmut_2,
        "xǁToolInstallerǁcreate_symlinks__mutmut_3": xǁToolInstallerǁcreate_symlinks__mutmut_3,
        "xǁToolInstallerǁcreate_symlinks__mutmut_4": xǁToolInstallerǁcreate_symlinks__mutmut_4,
        "xǁToolInstallerǁcreate_symlinks__mutmut_5": xǁToolInstallerǁcreate_symlinks__mutmut_5,
        "xǁToolInstallerǁcreate_symlinks__mutmut_6": xǁToolInstallerǁcreate_symlinks__mutmut_6,
        "xǁToolInstallerǁcreate_symlinks__mutmut_7": xǁToolInstallerǁcreate_symlinks__mutmut_7,
        "xǁToolInstallerǁcreate_symlinks__mutmut_8": xǁToolInstallerǁcreate_symlinks__mutmut_8,
        "xǁToolInstallerǁcreate_symlinks__mutmut_9": xǁToolInstallerǁcreate_symlinks__mutmut_9,
        "xǁToolInstallerǁcreate_symlinks__mutmut_10": xǁToolInstallerǁcreate_symlinks__mutmut_10,
        "xǁToolInstallerǁcreate_symlinks__mutmut_11": xǁToolInstallerǁcreate_symlinks__mutmut_11,
        "xǁToolInstallerǁcreate_symlinks__mutmut_12": xǁToolInstallerǁcreate_symlinks__mutmut_12,
        "xǁToolInstallerǁcreate_symlinks__mutmut_13": xǁToolInstallerǁcreate_symlinks__mutmut_13,
    }

    def create_symlinks(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁToolInstallerǁcreate_symlinks__mutmut_orig"),
            object.__getattribute__(self, "xǁToolInstallerǁcreate_symlinks__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    create_symlinks.__signature__ = _mutmut_signature(xǁToolInstallerǁcreate_symlinks__mutmut_orig)
    xǁToolInstallerǁcreate_symlinks__mutmut_orig.__name__ = "xǁToolInstallerǁcreate_symlinks"


# <3 🧱🤝🔧🪄
