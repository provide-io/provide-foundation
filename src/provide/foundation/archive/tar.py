#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from pathlib import Path
import tarfile

from attrs import define

from provide.foundation.archive.base import (
    ArchiveError,
    ArchiveFormatError,
    ArchiveIOError,
    ArchiveValidationError,
    BaseArchive,
)
from provide.foundation.archive.defaults import (
    DEFAULT_ARCHIVE_DETERMINISTIC,
    DEFAULT_ARCHIVE_PRESERVE_METADATA,
    DEFAULT_ARCHIVE_PRESERVE_PERMISSIONS,
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

"""TAR archive implementation."""

log = get_logger(__name__)


def deterministic_filter(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo:
    """Tarfile filter for deterministic/reproducible archives.

    Resets user/group info and modification time to ensure consistent
    output for reproducible builds.

    Args:
        tarinfo: TarInfo object to modify

    Returns:
        Modified TarInfo object with deterministic metadata

    Examples:
        >>> import tarfile
        >>> with tarfile.open("archive.tar", "w") as tar:
        ...     tar.add("myfile.txt", filter=deterministic_filter)

    Notes:
        This filter sets:
        - uid/gid to 0 (root)
        - uname/gname to empty strings
        - mtime to 0 (1970-01-01)

        This ensures archives are byte-for-byte identical when created
        from the same source, regardless of filesystem timestamps or
        ownership.
    """
    # Reset user/group info
    tarinfo.uid = 0
    tarinfo.gid = 0
    tarinfo.uname = ""
    tarinfo.gname = ""

    # Reset modification time
    tarinfo.mtime = 0

    return tarinfo


@define(slots=True)
class TarArchive(BaseArchive):
    """TAR archive implementation.

    Creates and extracts TAR archives with optional metadata preservation
    and deterministic output for reproducible builds.
    """

    deterministic: bool = field(default=DEFAULT_ARCHIVE_DETERMINISTIC)
    preserve_metadata: bool = field(default=DEFAULT_ARCHIVE_PRESERVE_METADATA)
    preserve_permissions: bool = field(default=DEFAULT_ARCHIVE_PRESERVE_PERMISSIONS)

    def create(self, source: Path, output: Path) -> Path:
        """Create TAR archive from source.

        Args:
            source: Source file or directory to archive
            output: Output TAR file path

        Returns:
            Path to created archive

        Raises:
            ArchiveError: If archive creation fails

        """
        try:
            ensure_parent_dir(output)

            with tarfile.open(output, "w") as tar:
                if source.is_dir():
                    # Add all files in directory (consistent with ZIP behavior)
                    for item in sorted(source.rglob("*")):
                        if item.is_file():
                            arcname = item.relative_to(source)
                            self._add_file(tar, item, arcname)
                else:
                    # Add single file
                    self._add_file(tar, source, source.name)

            log.debug(f"Created TAR archive: {output}")
            return output

        except OSError as e:
            raise ArchiveIOError(f"Failed to create TAR archive (I/O error): {e}") from e
        except Exception as e:
            raise ArchiveError(f"Failed to create TAR archive: {e}") from e

    def extract(self, archive: Path, output: Path, limits: ArchiveLimits | None = None) -> Path:  # noqa: C901
        """Extract TAR archive to output directory with decompression bomb protection.

        Args:
            archive: TAR archive file path
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

            with tarfile.open(archive, "r") as tar:
                # Enhanced security check - prevent path traversal and validate members
                safe_members = []
                for member in tar.getmembers():
                    # Check file count limit
                    tracker.check_file_count(1)

                    # Validate member size and compression ratio
                    tracker.validate_member_size(member.size)

                    # Track extracted size
                    tracker.add_extracted_size(member.size)

                    # Use unified path validation
                    if not is_safe_path(output, member.name):
                        raise ArchiveValidationError(
                            f"Unsafe path in archive: {member.name}. "
                            "Archive may contain path traversal, symlinks, or absolute paths."
                        )

                    # Additional checks for symlinks and hardlinks
                    if member.islnk() or member.issym():
                        # Check that link targets are also safe
                        if not is_safe_path(output, member.linkname):
                            raise ArchiveValidationError(
                                f"Unsafe link target in archive: {member.name} -> {member.linkname}. "
                                "Link target may escape extraction directory."
                            )

                        # Prevent absolute path in link target
                        if Path(member.linkname).is_absolute():
                            raise ArchiveValidationError(
                                f"Absolute path in link target: {member.name} -> {member.linkname}"
                            )

                    safe_members.append(member)

                # Check overall compression ratio
                tracker.check_compression_ratio()

                # Extract only validated members (all members have been security-checked above)
                tar.extractall(output, members=safe_members)  # nosec B202

            log.debug(f"Extracted TAR archive to: {output}")
            return output

        except (ArchiveError, ArchiveValidationError):
            raise
        except tarfile.ReadError as e:
            raise ArchiveFormatError(f"Invalid or corrupted TAR archive: {e}") from e
        except OSError as e:
            raise ArchiveIOError(f"Failed to extract TAR archive (I/O error): {e}") from e
        except Exception as e:
            raise ArchiveError(f"Failed to extract TAR archive: {e}") from e

    def validate(self, archive: Path) -> bool:
        """Validate TAR archive integrity.

        Args:
            archive: TAR archive file path

        Returns:
            True if archive is valid, False otherwise

        Note: This method intentionally catches all exceptions and returns False.
        This is NOT an error suppression case - returning False on any exception
        is the expected validation behavior. Do NOT replace this with @resilient decorator.
        """
        try:
            with tarfile.open(archive, "r") as tar:
                # Try to read all members
                for _member in tar.getmembers():
                    # Just checking we can read the metadata
                    pass
            return True
        except Exception:  # nosec B110
            # Broad catch is intentional for validation: any error means invalid archive.
            # Possible exceptions: tarfile.ReadError, OSError, PermissionError, etc.
            return False

    def list_contents(self, archive: Path) -> list[str]:
        """List contents of TAR archive.

        Args:
            archive: TAR archive file path

        Returns:
            List of file paths in archive

        Raises:
            ArchiveError: If listing fails

        """
        try:
            contents = []
            with tarfile.open(archive, "r") as tar:
                for member in tar.getmembers():
                    if member.isfile():
                        contents.append(member.name)
            return sorted(contents)
        except tarfile.ReadError as e:
            raise ArchiveFormatError(f"Invalid or corrupted TAR archive: {e}") from e
        except OSError as e:
            raise ArchiveIOError(f"Failed to list TAR contents (I/O error): {e}") from e
        except Exception as e:
            raise ArchiveError(f"Failed to list TAR contents: {e}") from e

    def _add_file(self, tar: tarfile.TarFile, file_path: Path, arcname: str | Path) -> None:
        """Add single file to TAR archive.

        Args:
            tar: Open TarFile object
            file_path: Path to file to add
            arcname: Name in archive

        """
        tarinfo = tar.gettarinfo(str(file_path), str(arcname))

        # Apply deterministic filter if enabled
        if self.deterministic:
            tarinfo = deterministic_filter(tarinfo)

        # Normalize permissions if requested
        if not self.preserve_permissions:
            if tarinfo.isfile():
                tarinfo.mode = 0o644
            elif tarinfo.isdir():
                tarinfo.mode = 0o755

        with file_path.open("rb") as f:
            tar.addfile(tarinfo, f)


# 🧱🏗️🔚
