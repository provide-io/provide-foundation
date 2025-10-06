from __future__ import annotations

import os
from pathlib import Path
import zipfile

from attrs import Attribute, define, validators

from provide.foundation.archive.base import ArchiveError, BaseArchive
from provide.foundation.config import defaults
from provide.foundation.config.base import field
from provide.foundation.file import ensure_parent_dir
from provide.foundation.logger import get_logger

"""ZIP archive implementation."""

logger = get_logger(__name__)


def _is_safe_path(base_dir: Path, target_path: str) -> bool:
    """Validate that a path is safe for extraction.

    Prevents:
    - Path traversal attacks (..)
    - Absolute paths
    - Symlinks that point outside base directory

    Args:
        base_dir: Base extraction directory
        target_path: Path to validate

    Returns:
        True if path is safe, False otherwise
    """
    # Check for absolute paths
    if Path(target_path).is_absolute():
        return False

    # Check for path traversal patterns
    if ".." in Path(target_path).parts:
        return False

    # Normalize and resolve the full path
    try:
        full_path = (base_dir / target_path).resolve()
        base_resolved = base_dir.resolve()

        # Ensure the resolved path is within base directory
        # This catches symlinks and other tricks
        return str(full_path).startswith(str(base_resolved) + os.sep) or full_path == base_resolved
    except (ValueError, OSError):
        return False


def _validate_compression_level(instance: ZipArchive, attribute: Attribute[int], value: int) -> None:
    """Validate compression level is between 0 and 9."""
    if not 0 <= value <= 9:
        raise ValueError(f"Compression level must be 0-9, got {value}")


@define(slots=True)
class ZipArchive(BaseArchive):
    """ZIP archive implementation.

    Creates and extracts ZIP archives with optional compression and encryption.
    Supports adding files to existing archives.
    """

    compression_level: int = field(
        default=defaults.DEFAULT_ZIP_COMPRESSION_LEVEL,
        validator=validators.and_(validators.instance_of(int), _validate_compression_level),
    )  # Compression level 0-9 (0=store, 9=best)
    compression_type: int = field(default=defaults.DEFAULT_ZIP_COMPRESSION_TYPE)
    password: bytes | None = field(default=defaults.DEFAULT_ZIP_PASSWORD)

    def create(self, source: Path, output: Path) -> Path:
        """Create ZIP archive from source.

        Args:
            source: Source file or directory to archive
            output: Output ZIP file path

        Returns:
            Path to created archive

        Raises:
            ArchiveError: If archive creation fails

        """
        try:
            ensure_parent_dir(output)

            with zipfile.ZipFile(
                output,
                "w",
                compression=self.compression_type,
                compresslevel=self.compression_level,
            ) as zf:
                if self.password:
                    zf.setpassword(self.password)

                if source.is_dir():
                    # Add all files in directory
                    for item in sorted(source.rglob("*")):
                        if item.is_file():
                            arcname = item.relative_to(source)
                            zf.write(item, arcname)
                else:
                    # Add single file
                    zf.write(source, source.name)

            logger.debug(f"Created ZIP archive: {output}")
            return output

        except Exception as e:
            raise ArchiveError(f"Failed to create ZIP archive: {e}") from e

    def extract(self, archive: Path, output: Path) -> Path:
        """Extract ZIP archive to output directory.

        Args:
            archive: ZIP archive file path
            output: Output directory path

        Returns:
            Path to extraction directory

        Raises:
            ArchiveError: If extraction fails or archive contains unsafe paths

        """
        try:
            output.mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(archive, "r") as zf:
                if self.password:
                    zf.setpassword(self.password)

                # Enhanced security check - prevent path traversal, symlinks, absolute paths
                for info in zf.infolist():
                    # Basic path safety check
                    if not _is_safe_path(output, info.filename):
                        raise ArchiveError(
                            f"Unsafe path in archive: {info.filename}. "
                            "Archive may contain path traversal, symlinks, or absolute paths."
                        )

                    # Check for symlinks (Unix file mode in external_attr)
                    # ZIP stores Unix permissions in the high 16 bits of external_attr
                    # Symlink mode is 0o120000 (S_IFLNK)
                    if info.external_attr:
                        mode = info.external_attr >> 16
                        is_symlink = (mode & 0o170000) == 0o120000  # S_IFLNK check

                        if is_symlink:
                            # Read the symlink target from the ZIP data
                            link_target = zf.read(info.filename).decode("utf-8")

                            # Validate the link target is safe
                            if not _is_safe_path(output, link_target):
                                raise ArchiveError(
                                    f"Unsafe symlink target in archive: {info.filename} -> {link_target}. "
                                    "Link target may escape extraction directory."
                                )

                            # Prevent absolute paths in link target
                            if Path(link_target).is_absolute():
                                raise ArchiveError(
                                    f"Absolute path in symlink target: {info.filename} -> {link_target}"
                                )

                # Extract all (all members have been security-checked above)
                zf.extractall(output)

            logger.debug(f"Extracted ZIP archive to: {output}")
            return output

        except ArchiveError:
            raise
        except Exception as e:
            raise ArchiveError(f"Failed to extract ZIP archive: {e}") from e

    def validate(self, archive: Path) -> bool:
        """Validate ZIP archive integrity.

        Args:
            archive: ZIP archive file path

        Returns:
            True if archive is valid, False otherwise

        """
        try:
            with zipfile.ZipFile(archive, "r") as zf:
                # Test the archive
                result = zf.testzip()
                return result is None  # None means no bad files
        except Exception:
            return False

    def list_contents(self, archive: Path) -> list[str]:
        """List contents of ZIP archive.

        Args:
            archive: ZIP archive file path

        Returns:
            List of file paths in archive

        Raises:
            ArchiveError: If listing fails

        """
        try:
            with zipfile.ZipFile(archive, "r") as zf:
                return sorted(zf.namelist())
        except Exception as e:
            raise ArchiveError(f"Failed to list ZIP contents: {e}") from e

    def add_file(self, archive: Path, file: Path, arcname: str | None = None) -> None:
        """Add file to existing ZIP archive.

        Args:
            archive: ZIP archive file path
            file: File to add
            arcname: Name in archive (defaults to file name)

        Raises:
            ArchiveError: If adding file fails

        """
        try:
            with zipfile.ZipFile(archive, "a", compression=self.compression_type) as zf:
                if self.password:
                    zf.setpassword(self.password)

                zf.write(file, arcname or file.name)

            logger.debug(f"Added {file} to ZIP archive {archive}")

        except Exception as e:
            raise ArchiveError(f"Failed to add file to ZIP: {e}") from e

    def extract_file(self, archive: Path, member: str, output: Path) -> Path:
        """Extract single file from ZIP archive.

        Args:
            archive: ZIP archive file path
            member: Name of file in archive
            output: Output directory or file path

        Returns:
            Path to extracted file

        Raises:
            ArchiveError: If extraction fails or member path is unsafe

        """
        try:
            with zipfile.ZipFile(archive, "r") as zf:
                if self.password:
                    zf.setpassword(self.password)

                # Enhanced security check
                extract_base = output if output.is_dir() else output.parent
                if not _is_safe_path(extract_base, member):
                    raise ArchiveError(
                        f"Unsafe path: {member}. Path may contain traversal, symlinks, or absolute paths."
                    )

                # Check for symlinks
                info = zf.getinfo(member)
                if info.external_attr:
                    mode = info.external_attr >> 16
                    is_symlink = (mode & 0o170000) == 0o120000  # S_IFLNK check

                    if is_symlink:
                        # Read the symlink target
                        link_target = zf.read(member).decode("utf-8")

                        # Validate the link target is safe
                        if not _is_safe_path(extract_base, link_target):
                            raise ArchiveError(
                                f"Unsafe symlink target: {member} -> {link_target}. "
                                "Link target may escape extraction directory."
                            )

                        # Prevent absolute paths in link target
                        if Path(link_target).is_absolute():
                            raise ArchiveError(f"Absolute path in symlink target: {member} -> {link_target}")

                if output.is_dir():
                    zf.extract(member, output)
                    return output / member
                ensure_parent_dir(output)
                with zf.open(member) as source, output.open("wb") as target:
                    target.write(source.read())
                return output

        except ArchiveError:
            raise
        except Exception as e:
            raise ArchiveError(f"Failed to extract file from ZIP: {e}") from e
