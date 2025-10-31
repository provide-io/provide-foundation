#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from pathlib import Path
import zipfile

from attrs import Attribute, define, validators

from provide.foundation.archive.base import (
    ArchiveError,
    ArchiveFormatError,
    ArchiveIOError,
    ArchiveValidationError,
    BaseArchive,
)
from provide.foundation.archive.defaults import (
    DEFAULT_ZIP_COMPRESSION_LEVEL,
    DEFAULT_ZIP_COMPRESSION_TYPE,
    DEFAULT_ZIP_PASSWORD,
)
from provide.foundation.archive.limits import (
    DEFAULT_LIMITS,
    ArchiveLimits,
    ExtractionTracker,
    get_archive_size,
)
from provide.foundation.archive.security import is_safe_path
from provide.foundation.config.base import field
from provide.foundation.file import ensure_parent_dir
from provide.foundation.logger import get_logger

"""ZIP archive implementation."""

log = get_logger(__name__)


def _validate_compression_level(instance: ZipArchive, attribute: Attribute[int], value: int) -> None:
    """Validate ZIP compression level is between 0 and 9.

    Note: ZIP supports level 0 (store, no compression) unlike other compressors
    which enforce 1-9. This is intentional and required for ZIP_STORED mode.
    """
    if not 0 <= value <= 9:
        raise ValueError(f"ZIP compression level must be 0-9, got {value}")


@define(slots=True)
class ZipArchive(BaseArchive):
    """ZIP archive implementation.

    Creates and extracts ZIP archives with optional compression.
    Supports adding files to existing archives.

    Security Note - Password Handling:
        The `password` parameter only decrypts existing encrypted ZIP files during
        extraction/reading. It does NOT encrypt new files during creation with
        stdlib zipfile. To create encrypted ZIP archives, use a third-party library
        like `pyzipper` that supports AES encryption. The stdlib zipfile.setpassword()
        method only enables reading password-protected archives.

    Attributes:
        compression_level: ZIP compression level 0-9 (0=store/no compression, 9=best)
        compression_type: Compression type (zipfile.ZIP_DEFLATED, etc)
        password: Password for decrypting existing encrypted archives (read-only)
    """

    compression_level: int = field(
        default=DEFAULT_ZIP_COMPRESSION_LEVEL,
        validator=validators.and_(validators.instance_of(int), _validate_compression_level),
    )
    compression_type: int = field(default=DEFAULT_ZIP_COMPRESSION_TYPE)
    password: bytes | None = field(default=DEFAULT_ZIP_PASSWORD)

    def create(self, source: Path, output: Path) -> Path:
        """Create ZIP archive from source.

        Args:
            source: Source file or directory to archive
            output: Output ZIP file path

        Returns:
            Path to created archive

        Raises:
            ArchiveError: If archive creation fails

        Note:
            Files are NOT encrypted during creation even if password is set.
            The stdlib zipfile module does not support creating encrypted archives.
            Use pyzipper or similar for AES-encrypted ZIP creation.

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

            log.debug(f"Created ZIP archive: {output}")
            return output

        except OSError as e:
            raise ArchiveIOError(f"Failed to create ZIP archive (I/O error): {e}") from e
        except Exception as e:
            raise ArchiveError(f"Failed to create ZIP archive: {e}") from e

    def extract(self, archive: Path, output: Path, limits: ArchiveLimits | None = None) -> Path:
        """Extract ZIP archive to output directory with decompression bomb protection.

        Args:
            archive: ZIP archive file path
            output: Output directory path
            limits: Optional extraction limits (uses DEFAULT_LIMITS if None)

        Returns:
            Path to extraction directory

        Raises:
            ArchiveError: If extraction fails, archive contains unsafe paths, or exceeds limits

        """
        if limits is None:
            limits = DEFAULT_LIMITS

        try:
            output.mkdir(parents=True, exist_ok=True)

            # Initialize extraction tracker
            tracker = ExtractionTracker(limits)
            tracker.set_compressed_size(get_archive_size(archive))

            with zipfile.ZipFile(archive, "r") as zf:
                if self.password:
                    zf.setpassword(self.password)

                # Validate all members before extraction
                self._validate_zip_members(zf, output, tracker)

                # Check overall compression ratio
                tracker.check_compression_ratio()

                # Extract all (all members have been security-checked above)
                zf.extractall(output)

            log.debug(f"Extracted ZIP archive to: {output}")
            return output

        except (ArchiveError, ArchiveValidationError):
            raise
        except zipfile.BadZipFile as e:
            raise ArchiveFormatError(f"Invalid or corrupted ZIP archive: {e}") from e
        except OSError as e:
            raise ArchiveIOError(f"Failed to extract ZIP archive (I/O error): {e}") from e
        except Exception as e:
            raise ArchiveError(f"Failed to extract ZIP archive: {e}") from e

    def _validate_zip_members(self, zf: zipfile.ZipFile, output: Path, tracker: ExtractionTracker) -> None:
        """Validate all ZIP members for security and limits.

        Args:
            zf: Open ZipFile object
            output: Extraction output directory
            tracker: ExtractionTracker for tracking limits

        Raises:
            ArchiveError: If any member is invalid or exceeds limits

        """
        for info in zf.infolist():
            # Check file count limit
            tracker.check_file_count(1)

            # Validate member size and compression ratio
            tracker.validate_member_size(info.file_size, info.compress_size)

            # Track extracted size
            tracker.add_extracted_size(info.file_size)

            # Validate path safety
            self._validate_member_path(output, info.filename)

            # Check for and validate symlinks
            if info.external_attr:
                self._validate_symlink_if_present(zf, output, info)

    def _validate_member_path(self, output: Path, filename: str) -> None:
        """Validate that a ZIP member path is safe.

        Args:
            output: Extraction output directory
            filename: Member filename to validate

        Raises:
            ArchiveError: If path is unsafe (traversal, absolute, etc.)

        """
        if not is_safe_path(output, filename):
            raise ArchiveValidationError(
                f"Unsafe path in archive: {filename}. "
                "Archive may contain path traversal, symlinks, or absolute paths."
            )

    def _validate_symlink_if_present(self, zf: zipfile.ZipFile, output: Path, info: zipfile.ZipInfo) -> None:
        """Check if member is a symlink and validate if so.

        ZIP stores Unix permissions in the high 16 bits of external_attr.
        Symlink mode is 0o120000 (S_IFLNK).

        Args:
            zf: Open ZipFile object
            output: Extraction output directory
            info: ZipInfo for the member to check

        Raises:
            ArchiveError: If symlink target is unsafe

        """
        mode = info.external_attr >> 16
        is_symlink = (mode & 0o170000) == 0o120000  # S_IFLNK check

        if is_symlink:
            # Read the symlink target from the ZIP data
            link_target = zf.read(info.filename).decode("utf-8")

            # Validate the link target is safe
            if not is_safe_path(output, link_target):
                raise ArchiveValidationError(
                    f"Unsafe symlink target in archive: {info.filename} -> {link_target}. "
                    "Link target may escape extraction directory."
                )

            # Prevent absolute paths in link target
            if Path(link_target).is_absolute():
                raise ArchiveValidationError(
                    f"Absolute path in symlink target: {info.filename} -> {link_target}"
                )

    def validate(self, archive: Path) -> bool:
        """Validate ZIP archive integrity.

        Args:
            archive: ZIP archive file path

        Returns:
            True if archive is valid, False otherwise

        Note: This method intentionally catches all exceptions and returns False.
        This is NOT an error suppression case - returning False on any exception
        is the expected validation behavior. Do NOT replace this with @resilient decorator.
        """
        try:
            with zipfile.ZipFile(archive, "r") as zf:
                # Test the archive
                result = zf.testzip()
                return result is None  # None means no bad files
        except Exception:  # nosec B110
            # Broad catch is intentional for validation: any error means invalid archive.
            # Possible exceptions: zipfile.BadZipFile, OSError, PermissionError, etc.
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
        except zipfile.BadZipFile as e:
            raise ArchiveFormatError(f"Invalid or corrupted ZIP archive: {e}") from e
        except OSError as e:
            raise ArchiveIOError(f"Failed to list ZIP contents (I/O error): {e}") from e
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

            log.debug(f"Added {file} to ZIP archive {archive}")

        except OSError as e:
            raise ArchiveIOError(f"Failed to add file to ZIP (I/O error): {e}") from e
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
                self._validate_member_path(extract_base, member)

                # Check for symlinks
                info = zf.getinfo(member)
                if info.external_attr:
                    self._validate_symlink_if_present(zf, extract_base, info)

                if output.is_dir():
                    zf.extract(member, output)
                    return output / member
                ensure_parent_dir(output)
                with zf.open(member) as source, output.open("wb") as target:
                    target.write(source.read())
                return output

        except (ArchiveError, ArchiveValidationError):
            raise
        except zipfile.BadZipFile as e:
            raise ArchiveFormatError(f"Invalid or corrupted ZIP archive: {e}") from e
        except OSError as e:
            raise ArchiveIOError(f"Failed to extract file from ZIP (I/O error): {e}") from e
        except Exception as e:
            raise ArchiveError(f"Failed to extract file from ZIP: {e}") from e


# 🧱🏗️🔚
