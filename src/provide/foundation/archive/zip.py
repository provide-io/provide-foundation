from __future__ import annotations

from pathlib import Path
import zipfile

from attrs import define, field, validators

from provide.foundation.archive.base import ArchiveError, BaseArchive
from provide.foundation.file import ensure_parent_dir
from provide.foundation.logger import get_logger

"""ZIP archive implementation."""

logger = get_logger(__name__)


def _validate_compression_level(instance: object, attribute: object, value: int) -> None:
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
        default=6,
        validator=[validators.instance_of(int), _validate_compression_level],
    )  # Compression level 0-9 (0=store, 9=best)
    compression_type: int = field(default=zipfile.ZIP_DEFLATED)
    password: bytes | None = field(default=None)

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
            ArchiveError: If extraction fails

        """
        try:
            output.mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(archive, "r") as zf:
                if self.password:
                    zf.setpassword(self.password)

                # Security check - prevent path traversal
                for member in zf.namelist():
                    if member.startswith("/") or ".." in member:
                        raise ArchiveError(f"Unsafe path in archive: {member}")

                # Extract all
                zf.extractall(output)

            logger.debug(f"Extracted ZIP archive to: {output}")
            return output

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
            ArchiveError: If extraction fails

        """
        try:
            with zipfile.ZipFile(archive, "r") as zf:
                if self.password:
                    zf.setpassword(self.password)

                # Security check
                if member.startswith("/") or ".." in member:
                    raise ArchiveError(f"Unsafe path: {member}")

                if output.is_dir():
                    zf.extract(member, output)
                    return output / member
                ensure_parent_dir(output)
                with zf.open(member) as source, output.open("wb") as target:
                    target.write(source.read())
                return output

        except Exception as e:
            raise ArchiveError(f"Failed to extract file from ZIP: {e}") from e
