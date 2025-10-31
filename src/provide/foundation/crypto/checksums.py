#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from pathlib import Path

from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM
from provide.foundation.crypto.hashing import hash_data, hash_file
from provide.foundation.crypto.utils import compare_hash
from provide.foundation.errors.resources import ResourceError
from provide.foundation.logger import get_logger

"""Checksum verification and management."""

log = get_logger(__name__)


def verify_file(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def verify_data(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def calculate_checksums(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def parse_checksum_file(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def write_checksum_file(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def verify_checksum_file(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


# 🧱🏗️🔚
